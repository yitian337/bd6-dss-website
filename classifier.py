import os
import pandas as pd
import numpy as np
import joblib
import warnings
from datetime import datetime, timedelta
from scipy import signal, stats
from scipy.signal import find_peaks

# Suppress sklearn version warnings for a clean production console
warnings.filterwarnings("ignore", category=UserWarning)

# --- STRICT CONFIGURATION ---
# Order of SENSORS and SIGNAL_COLS is mathematically critical.
# Altering this list will misalign the 324 features expected by the SVM.
WINDOW = 240
FS = 120.0
SENSORS = ['Wrist', 'Forearm', 'Elbow', 'Shoulder']
SIGNAL_COLS = ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyr_X', 'Gyr_Y', 'Gyr_Z', 'Roll', 'Pitch', 'Yaw']
NEW_DATA_FOLDER = 'new_data'
RAW_DATA_FOLDER = 'raw_data'

# Load the fused 324-feature models
try:
    model = joblib.load('svm_model.pkl')
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError:
    print("CRITICAL ERROR: Model files not found in the directory.")

def find_header_line(filepath):
    """Scans the Xsens file to bypass variable-length metadata headers."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if 'PacketCounter' in line and 'Acc_X' in line:
                return i
    raise ValueError(f"Valid sensor header not found in {filepath}")

def bandpass_filter(x):
    """Applies a 3rd order Butterworth filter (0.1Hz - 12.0Hz)."""
    b, a = signal.butter(3, 12.0/(FS/2), btype='low')
    x = signal.filtfilt(b, a, x)
    b, a = signal.butter(3, 0.1/(FS/2), btype='high')
    return signal.filtfilt(b, a, x)

def compute_9_features(x):
    """Extracts the 9 core statistical metrics for a given signal."""
    x = x[~np.isnan(x)]
    if len(x) < 10: return [0.0] * 9
    
    hist, _ = np.histogram(x, bins=10, density=True)
    hist = hist[hist > 0]
    peaks, _ = find_peaks(np.abs(x))
    
    return [
        np.std(x),
        np.sqrt(np.mean(x**2)),
        -np.sum(hist * np.log2(hist + 1e-12)),
        np.sqrt(np.mean(np.diff(x)**2)),
        len(peaks),
        np.max(np.abs(x)),
        np.mean(np.abs(np.diff(x))),
        stats.kurtosis(x),
        stats.skew(x)
    ]

def classify_window_fused(window_slice):
    """
    Fuses all 4 sensors into a single 324-feature vector for SVM prediction.
    Calculates unified Jerk and ROM for clinical storage.
    """
    feat = []
    jerk_vals = []
    rom_vals = []
    
    # 1. Strict Feature Extraction (Must iterate in exact SENSORS order)
    for sname in SENSORS:
        df = window_slice[sname]
        for col in SIGNAL_COLS:
            if col in df.columns:
                sig = df[col].dropna().to_numpy(dtype=float)
                feat.extend(compute_9_features(bandpass_filter(sig)))
            else:
                feat.extend([0.0] * 9)
                
        # 2. Extract Medical Metrics simultaneously
        if 'Acc_X' in df.columns:
            ax = bandpass_filter(df['Acc_X'].dropna().to_numpy(dtype=float))
            jerk_vals.append(np.sqrt(np.mean(np.diff(ax)**2)))
            
        if all(c in df.columns for c in ['Acc_X', 'Acc_Y', 'Acc_Z']):
            acc_mag = np.sqrt(df['Acc_X']**2 + df['Acc_Y']**2 + df['Acc_Z']**2)
            rom_vals.append(acc_mag.mean())

    # 3. Model Prediction
    # Ensure strict shape mapping (1, 324)
    feat_array = np.array(feat).reshape(1, -1)
    prediction = model.predict(scaler.transform(feat_array))[0]
    
    mapping = {'A': 'Reach & Retrieve', 'B': 'Lift Cup', 'C': 'Swing Arm', 'D': 'Rotate Wrist'}
    movement = mapping.get(prediction, "Unknown")
    
    # 4. Finalize Metrics
    jerk = round(float(np.mean(jerk_vals)), 4) if jerk_vals else 0.0
    rom = round(float(np.mean(rom_vals)), 4) if rom_vals else 0.0
    risk = 'High' if (jerk >= 0.15 or rom <= 7.0) else ('Medium' if jerk >= 0.05 else 'Low')
    
    return movement, jerk, rom, risk

def add_new_data(patient_id, add_movement_fn):
    """
    Orchestrates the ingestion of a recording session.
    Parses files, strictly aligns time windows, predicts, and logs to DB.
    """
    os.makedirs(RAW_DATA_FOLDER, exist_ok=True)
    
    # 1. Data Ingestion & Sanitization
    sensor_dfs = {}
    for sname in SENSORS:
        # Assumes files are named exactly "Wrist.txt", etc.
        fpath = os.path.join(NEW_DATA_FOLDER, f"{sname}.txt")
        if not os.path.exists(fpath):
            print(f"Aborting: Missing essential sensor file '{sname}.txt'")
            return
            
        skip = find_header_line(fpath)
        df = pd.read_csv(fpath, sep='\t', skiprows=skip)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.loc[:, ~df.columns.str.contains(r'^Unnamed')]
        
        for col in SIGNAL_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        sensor_dfs[sname] = df

    # 2. Time Synchronization Safeguard
    min_len = min(len(df) for df in sensor_dfs.values())
    n_windows = min_len // WINDOW
    
    # 3. Dynamic Timestamp Calculation (Backtracking from file creation)
    # File modification time acts as the absolute end of the recording
    sample_file = os.path.join(NEW_DATA_FOLDER, f"{SENSORS[0]}.txt")
    end_dt = datetime.fromtimestamp(os.path.getmtime(sample_file))
    
    window_duration = WINDOW / FS  # Exactly 2.0 seconds
    total_duration = n_windows * window_duration
    start_dt = end_dt - timedelta(seconds=total_duration)

    print(f"Classifying {n_windows} synchronized windows (324-Feature Tensor)...")

    # 4. Pipeline Execution
    for i in range(n_windows):
        # Slice synchronized windows
        window_slice = {s: df.iloc[i*WINDOW : (i+1)*WINDOW] for s, df in sensor_dfs.items()}
        
        movement, jerk, rom, risk = classify_window_fused(window_slice)
        
        # Calculate exactly when this 2-second window began
        current_window_dt = start_dt + timedelta(seconds=i * window_duration)
        window_dt_str = current_window_dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Save Metadata to SQLite
        key = add_movement_fn(patient_id, window_dt_str, movement, rom, jerk, risk)
        
        # Save Raw Waveform to CSV for Streamlit Dashboards
        processed_dfs = []
        for sname in SENSORS:
            sdf = window_slice[sname].copy().reset_index(drop=True)
            sdf.columns = [f"{sname}_{col}" for col in sdf.columns]
            processed_dfs.append(sdf)
            
        raw_df = pd.concat(processed_dfs, axis=1)
        raw_df.to_csv(os.path.join(RAW_DATA_FOLDER, f"mov_{key}.csv"), index=False)

    print(f"Successfully processed {n_windows} movements. Timestamps incremented by 2s.")