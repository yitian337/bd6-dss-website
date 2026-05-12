import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime
from scipy import signal, stats
from scipy.signal import find_peaks

# --- Configuration ---
BASE = '.' 
WINDOW = 240
FS = 120.0
SIGNAL_COLS = ['Acc_X','Acc_Y','Acc_Z','Gyr_X','Gyr_Y','Gyr_Z','Roll','Pitch','Yaw']
SESSION_SENSORS = {'Wrist':'00B44802','Forearm':'00B44870','Elbow':'00B447FE','Shoulder':'00B4484B'}
NEW_DATA_FOLDER = 'new_data'
RAW_DATA_FOLDER = 'raw_data'

# Load the model data
model = joblib.load('svm_model.pkl')
scaler = joblib.load('scaler.pkl')

def find_header_line(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if 'PacketCounter' in line and 'Acc_X' in line:
                return i
    raise ValueError(f'Header not found: {path}')

def load_mt_file(path):
    h = find_header_line(path)
    df = pd.read_csv(path, skiprows=h, sep='\t', engine='python')
    df.columns = [str(c).strip() for c in df.columns]
    df = df.loc[:, ~df.columns.str.contains(r'^Unnamed')]
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def bandpass_filter(x, fs=FS):
    b, a = signal.butter(3, 12.0/(fs/2), btype='low')
    x = signal.filtfilt(b, a, x)
    b, a = signal.butter(3, 0.1/(fs/2), btype='high')
    x = signal.filtfilt(b, a, x)
    return x

def compute_9_features(x):
    x = x[~np.isnan(x)]
    if len(x) < 10: return [0.0]*9
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

def compute_risk(jerk, rom):
    if jerk >= 0.15 or rom <= 7.0: return 'High'
    elif jerk >= 0.05: return 'Medium'
    else: return 'Low'

def classify_window(sensor_dfs):
    """
    Extracts 81 features from the Wrist sensor to match the Model/Scaler.
    Calculates Jerk/ROM from all sensors for the medical report.
    """
    feat = []
    # 1. Feature Extraction
    wrist_df = sensor_dfs['Wrist']
    for col in SIGNAL_COLS:
        sig = wrist_df[col].dropna().to_numpy(dtype=float)
        feat += compute_9_features(bandpass_filter(sig))
    
    # 2. Prediction
    movement = model.predict(scaler.transform([feat]))[0]
    
    # 3. Quality Metrics
    jerk_vals, rom_vals = [], []
    for df in sensor_dfs.values():
        ax = bandpass_filter(df['Acc_X'].dropna().to_numpy(dtype=float))
        jerk_vals.append(np.sqrt(np.mean(np.diff(ax)**2)))
        
        # ROM approximation via Acc magnitude
        rom_vals.append(np.sqrt(np.mean(df['Acc_X']**2 + df['Acc_Y']**2 + df['Acc_Z']**2)))

    jerk = round(float(np.mean(jerk_vals)), 4)
    rom = round(float(np.mean(rom_vals)), 4)
    risk = compute_risk(jerk, rom)
    
    return movement, jerk, rom, risk

def get_raw_data(window_slice):
    rows = []
    for sname, df in window_slice.items():
        seg = df.reset_index(drop=True)
        for s_idx, row in seg.iterrows():
            rows.append({
                'sensor': sname, 'sample_index': s_idx,
                'Acc_X': row.get('Acc_X'), 'Acc_Y': row.get('Acc_Y'), 'Acc_Z': row.get('Acc_Z')
            })
    return pd.DataFrame(rows)

def add_new_data(patient_id, add_movement_fn):
    os.makedirs(RAW_DATA_FOLDER, exist_ok=True)
    
    # Load files matching SESSION_SENSORS
    sensor_dfs = {}
    for sname, sid in SESSION_SENSORS.items():
        fpath = os.path.join(NEW_DATA_FOLDER, f"{sname}.txt")
        if os.path.exists(fpath):
            sensor_dfs[sname] = load_mt_file(fpath)
            print(f'Loaded {sname}')
    
    if len(sensor_dfs) < 4:
        print("Error: Need all 4 sensor files (Wrist.txt, Forearm.txt, etc.)")
        return

    n_windows = len(list(sensor_dfs.values())[0]) // WINDOW
    session_dt = datetime.now().strftime('%Y-%m-%d %H:%M')

    for w_idx in range(n_windows):
        window_slice = {s: df.iloc[w_idx*WINDOW:(w_idx+1)*WINDOW] for s, df in sensor_dfs.items()}
        
        try:
            # Analyze window
            movement, jerk, rom, risk = classify_window(window_slice)
            
            key = add_movement_fn(patient_id, session_dt, movement, rom, jerk, risk)
            
            # Save raw data for later plotting
            raw_df = get_raw_data(window_slice)
            raw_df.to_csv(os.path.join(RAW_DATA_FOLDER, f'mov_{key}.csv'), index=False)
            print(f'Window {w_idx} -> {movement} (Risk: {risk}) saved.')
            
        except Exception as e:
            print(f'Error in window {w_idx}: {e}')

print("Pipeline Ready.")