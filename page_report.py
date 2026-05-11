import os
from pathlib import Path
import streamlit as st
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
            st.markdown('<div class="section-title">Classified Movement History</div>', unsafe_allow_html=True)

        with right:
            with st.container(key="back_wrap"):
                if st.button("← Back", key="back_btn", use_container_width=True):
                    st.session_state.selected_patient = patient
                    st.session_state.page = "patient"
                    st.rerun()

    movements = get_patient_movements(patient[0])

    if not movements:
        st.info("No movements recorded for this patient yet.")
    else:
        # Create table data
        table_data = []
        for movement in movements:
            movement_id, datetime_str, movement_type, risk_level = movement
            # Parse datetime string
            dt = datetime.fromisoformat(datetime_str)
            day = dt.strftime("%Y-%m-%d")
            time_str = dt.strftime("%H:%M:%S")
            table_data.append({
                "Day": day,
                "Time": time_str,
                "Risk": risk_level,
                "Movement": movement_type,
                "ID": movement_id
            })

        # Display table with columns
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1.2], gap="medium")

        with col1:
            st.markdown('<div class="metric-label" style="text-align: left;"><b>Day</b></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-label"><b>Time</b></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-label"><b>Risk</b></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-label"><b>Action</b></div>', unsafe_allow_html=True)

        st.divider()

        for idx, row in enumerate(table_data):
            col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1.2], gap="medium")

            with col1:
                st.markdown(f'<div class="summary-value">{row["Day"]}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="summary-value">{row["Time"]}</div>', unsafe_allow_html=True)
            with col3:
                risk_color = "#d32f2f" if row["Risk"] == "High" else "#f57c00" if row["Risk"] == "Medium" else "#388e3c"
                st.markdown(f'<div class="summary-value" style="color: {risk_color}; font-weight: bold;">{row["Risk"]}</div>', unsafe_allow_html=True)
            with col4:
                if st.button("View Details", key=f"view_movement_{row['ID']}", use_container_width=True):
                    st.session_state.selected_movement = row['ID']
                    st.toast(f"Viewing movement {row['Movement']}")

