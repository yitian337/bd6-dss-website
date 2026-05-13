import os
from pathlib import Path
import streamlit as st
import pandas as pd
from data import *
from datetime import datetime
import time

def show():
    patient = st.session_state.selected_patient
    
    patient_id = f"{patient[0]:04d}"
    name = patient[1]
    gender = patient[2]
    age = patient[3]

    # # -----------------------------
    # # Top card
    # # -----------------------------

    with st.container(key="st-patient_info_card"):
    
        left, middle, x, right = st.columns([2, 1, 1, 1], gap="medium")

        with left:
            icon, info = st.columns([1, 2], gap="medium", vertical_alignment="center")

            with icon:
                img_path = Path(__file__).with_name('icon.png')
                if not os.path.exists(img_path):
                    display_img = f"https://ui-avatars.com/api/?name={name}&background=dbe7f3&color=1f4e79&bold=true&size=128"
                else:
                    display_img = img_path

                st.markdown('<div class="patient-img">', unsafe_allow_html=True)
                st.image(display_img, width='content')
                st.markdown('</div>', unsafe_allow_html=True)

            with info:
                st.markdown(f"""
                    <div class="patient-meta">
                        ID: {patient_id}<br>
                        Name: {name}<br>
                        Gender: {gender}<br>
                        Age: {age}<br>
                    </div>
                """, unsafe_allow_html=True)
        
        with middle:
            st.markdown('<div class="section-title">Exercise History</div>', unsafe_allow_html=True)

        with right:
            if st.button("← Back", key="back_btn", use_container_width=True):
                st.session_state.selected_patient = patient
                st.session_state.page = "patient"
                st.rerun()

    # # -----------------------------
    # # Table
    # # -----------------------------

    movements = get_patient_movements(patient[0])

    if not movements:
        st.info("No movements recorded for this patient yet.")
    else:
        # Create table data
        table_data = []
        for movement in movements:
            movement_id, datetime_str, movement_type, rom_value, jerk_value, risk_level = movement
            # Parse datetime string
            dt = datetime.fromisoformat(datetime_str)
            day = dt.strftime("%Y-%m-%d")
            time_str = dt.strftime("%H:%M:%S")
            table_data.append({
                "Day": day,
                "Time": time_str,
                "Movement": movement_type,
                "ROM": rom_value,
                "Jerk": jerk_value,
                "Risk": risk_level,
                "ID": movement_id
            })

        # Display header
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.2, 1.0, 1.2, 0.8, 0.8, 1.0, 1.0], gap="small")
        with col1:
            st.markdown('<div style="font-weight: bold;">Day</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="font-weight: bold;">Time</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div style="font-weight: bold;">Movement</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div style="font-weight: bold;">ROM</div>', unsafe_allow_html=True)
        with col5:
            st.markdown('<div style="font-weight: bold;">Jerk</div>', unsafe_allow_html=True)
        with col6:
            st.markdown('<div style="font-weight: bold;">Risk</div>', unsafe_allow_html=True)
        with col7:
            st.markdown('<div style="font-weight: bold;">View</div>', unsafe_allow_html=True)

        st.divider()

        # Display each row with data and inline buttons
        for idx, row in enumerate(table_data):
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1.2, 1.0, 1.2, 0.8, 0.8, 1.0, 1.0], gap="small")

            with col1:
                st.markdown(f'<div>{row["Day"]}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div>{row["Time"]}</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div>{row["Movement"]}</div>', unsafe_allow_html=True)
            with col4:
                rom_val = f'{row["ROM"]:.2f}' if row["ROM"] is not None else 'N/A'
                st.markdown(f'<div>{rom_val}</div>', unsafe_allow_html=True)
            with col5:
                jerk_val = f'{row["Jerk"]:.2f}' if row["Jerk"] is not None else 'N/A'
                st.markdown(f'<div>{jerk_val}</div>', unsafe_allow_html=True)
            with col6:
                risk_color = "#d32f2f" if row["Risk"] == "High" else "#f57c00" if row["Risk"] == "Medium" else "#388e3c"
                st.markdown(f'<div style="color: {risk_color}; font-weight: bold;">{row["Risk"]}</div>', unsafe_allow_html=True)
            with col7:
                if st.button("View Raw Data", key=f"view_raw_{row['ID']}", use_container_width=True):
                    st.session_state.viewing_movement_id = row['ID']

    # # -----------------------------
    # # Raw Data Visualization (Modal)
    # # -----------------------------

    if "viewing_movement_id" in st.session_state and st.session_state.viewing_movement_id:
        @st.dialog("Raw Sensor Data", width="large")
        def show_raw_data_modal():
            mov_id = st.session_state.viewing_movement_id
            csv_path = Path(__file__).parent / "raw_data" / f"mov_{mov_id}.csv"
            
            st.write(f"**Movement ID:** {mov_id}")
            
            if csv_path.exists():
                try:
                    df = pd.read_csv(csv_path)
                    
                    # Detect available sensors from column names
                    sensor_order = ['Wrist', 'Forearm', 'Elbow', 'Shoulder']
                    available_sensors = []
                    for sensor in sensor_order:
                        if any(col.startswith(sensor + '_') for col in df.columns):
                            available_sensors.append(sensor)
                    
                    if not available_sensors:
                        st.warning("No sensor data found in CSV")
                        return
                    
                    cols = st.columns(min(4, len(available_sensors)))
                    
                    for idx, sensor in enumerate(available_sensors):
                        with cols[idx]:
                            st.markdown(f"**{sensor}**")
                            
                            # Extract accelerometer columns for this sensor
                            acc_x_col = f'{sensor}_Acc_X'
                            acc_y_col = f'{sensor}_Acc_Y'
                            acc_z_col = f'{sensor}_Acc_Z'
                            
                            # Check if columns exist
                            if acc_x_col in df.columns and acc_y_col in df.columns and acc_z_col in df.columns:
                                chart_data = pd.DataFrame({
                                    'X': df[acc_x_col],
                                    'Y': df[acc_y_col],
                                    'Z': df[acc_z_col]
                                })
                                
                                st.line_chart(chart_data)
                            else:
                                st.warning(f"Accelerometer data not found for {sensor}")
                
                except Exception as e:
                    st.error(f"Error loading raw data: {e}")
            else:
                st.warning(f"Raw data file not found: mov_{mov_id}.csv")
        
        show_raw_data_modal()
