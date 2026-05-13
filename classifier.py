import os
import pandas as pd
import numpy as np
import joblib
import warnings
from datetime import datetime, timedelta
from scipy import signal, stats
from scipy.signal import find_peaks

# Suppress sklearn version warnings
warnings.filterwarnings("ignore", category=UserWarning)

# --- CONFIGURATION ---
WINDOW = 240
FS = 120.0
SENSORS = ['Wrist', 'Forearm', 'Elbow', 'Shoulder']
SIGNAL_COLS = ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyr_X', 'Gyr_Y', 'Gyr_Z', 'Roll', 'Pitch', 'Yaw']
RAW_DATA_FOLDER = 'raw_data'

# --- ABSOLUTE PATH RESOLUTION ---
# Justification: Streamlit's execution context can change. Using __file__ ensures
# we look in the folder where THIS script lives, not where the terminal was opened.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'svm_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')

def load_system_assets():
    """Strict asset loader to prevent NameErrors."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(
            f"Asset Load Failure: Files not found at {BASE_DIR}. "
            "Ensure 'svm_model.pkl' and 'scaler.pkl' are in the same folder as classifier.py"
        )
    return joblib.load(MODEL_PATH), joblib.load(SCALER_PATH)

# Global initialization
# Justification: Loading here ensures the model is in memory once, not reloaded every window.
try:
    model, scaler = load_system_assets()
except Exception as e:
    model, scaler = None, None
    print(f"CRITICAL BOOT ERROR: {e}")

def find_header_line(file_obj):
    """
    Scans a file stream to find the header.
    Justification: file_obj.seek(0) is mandatory because file-like objects 
    maintain a 'cursor'. We must reset it before and after scanning.
    """
    file_obj.seek(0)
    # Streamlit UploadedFile can be bytes; we decode to string for matching
    for i, line in enumerate(file_obj):
        line_str = line.decode('utf-8') if isinstance(line, bytes) else line
        if 'PacketCounter' in line_str and 'Acc_X' in line_str:
            file_obj.seek(0) # Reset pointer for pandas
            return i
    file_obj.seek(0)
    raise ValueError("Valid sensor header not found in the uploaded file.")

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
    """Fuses all 4 sensors into a 324-feature vector for SVM prediction."""
    # Justification: Explicitly check for model existence before use to provide clean error.
    if model is None or scaler is None:
        raise RuntimeError("Classification engine is not initialized. Check console for boot errors.")

    feat = []
    jerk_vals = []
    rom_vals = []
    
    for sname in SENSORS:
        df = window_slice[sname]
        for col in SIGNAL_COLS:
            if col in df.columns:
                sig = df[col].dropna().to_numpy(dtype=float)
                feat.extend(compute_9_features(bandpass_filter(sig)))
            else:
                feat.extend([0.0] * 9)
                
        if 'Acc_X' in df.columns:
            ax = bandpass_filter(df['Acc_X'].dropna().to_numpy(dtype=float))
            jerk_vals.append(np.sqrt(np.mean(np.diff(ax)**2)))
            
        if all(c in df.columns for c in ['Acc_X', 'Acc_Y', 'Acc_Z']):
            acc_mag = np.sqrt(df['Acc_X']**2 + df['Acc_Y']**2 + df['Acc_Z']**2)
            rom_vals.append(acc_mag.mean())

    feat_array = np.array(feat).reshape(1, -1)
    prediction = model.predict(scaler.transform(feat_array))[0]
    
    mapping = {'A': 'Reach & Retrieve', 'B': 'Lift Cup', 'C': 'Swing Arm', 'D': 'Rotate Wrist'}
    movement = mapping.get(prediction, "Unknown")
    
    jerk = round(float(np.mean(jerk_vals)), 4) if jerk_vals else 0.0
    rom = round(float(np.mean(rom_vals)), 4) if rom_vals else 0.0
    risk = 'High' if (jerk >= 0.15 or rom <= 7.0) else ('Medium' if jerk >= 0.05 else 'Low')
    
    return movement, jerk, rom, risk

def add_new_data(patient_id, file_dict, add_movement_fn):
    """Ingests data from Streamlit's UploadedFile objects."""
    os.makedirs(RAW_DATA_FOLDER, exist_ok=True)
    
    sensor_dfs = {}
    for sname in SENSORS:
        uploaded_file = file_dict.get(sname)
        if uploaded_file is None:
            raise ValueError(f"Incomplete dataset: '{sname}' data was not uploaded.")
            
        skip = find_header_line(uploaded_file)
        # Justification: seek(0) is called inside find_header_line, 
        # so we can read the CSV starting from the beginning.
        df = pd.read_csv(uploaded_file, sep='\t', skiprows=skip)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.loc[:, ~df.columns.str.contains(r'^Unnamed')]
        
        for col in SIGNAL_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        sensor_dfs[sname] = df

    min_len = min(len(df) for df in sensor_dfs.values())
    n_windows = min_len // WINDOW
    
    # Timing logic: Backtrack from current time as file metadata isn't reliable on upload
    end_dt = datetime.now()
    window_duration = WINDOW / FS 
    start_dt = end_dt - timedelta(seconds=n_windows * window_duration)

    for i in range(n_windows):
        window_slice = {s: df.iloc[i*WINDOW : (i+1)*WINDOW] for s, df in sensor_dfs.items()}
        movement, jerk, rom, risk = classify_window_fused(window_slice)
        
        current_window_dt = start_dt + timedelta(seconds=i * window_duration)
        window_dt_str = current_window_dt.strftime('%Y-%m-%d %H:%M:%S')
        
        key = add_movement_fn(patient_id, window_dt_str, movement, rom, jerk, risk)
        
        processed_dfs = []
        for sname in SENSORS:
            sdf = window_slice[sname].copy().reset_index(drop=True)
            sdf.columns = [f"{sname}_{col}" for col in sdf.columns]
            processed_dfs.append(sdf)
            
        raw_df = pd.concat(processed_dfs, axis=1)
        raw_df.to_csv(os.path.join(RAW_DATA_FOLDER, f"mov_{key}.csv"), index=False)

    return n_windows