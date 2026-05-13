from pathlib import Path
import streamlit as st
import os
from datetime import datetime
from data import *
import pandas as pd


def show():
    
    st.markdown('<div class="main-title">Patient Selection</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    left, middle, right = st.columns([1, 4, 1], gap="medium")
    with left:
        with st.popover("Add Patient", use_container_width=True):
            with st.form("add_patient", clear_on_submit=True, enter_to_submit=False):
                np_name = st.text_input("Name")
                np_gender = st.selectbox("Gender", ["M", "F", "X"])
                np_dob = st.text_input("Date of Birth (YYYY-MM-DD)")
                submit_btn = st.form_submit_button("Enter", width="stretch")
                if submit_btn:
                    if np_name and np_gender and np_dob:
                        # Validate DOB format
                        try:
                            datetime.strptime(np_dob, "%Y-%m-%d")
                            add_patient(np_name, np_gender, np_dob)
                            st.toast(f"Patient {np_name} added")
                            st.rerun()
                        except ValueError:
                            st.error("Invalid date format. Please use YYYY-MM-DD (e.g., 1995-03-15)")
                    else:
                        st.error("Please fill in all fields.")
    
    with right:
        if st.button("← Back", key="back_btn", use_container_width=True):
                        st.session_state.selected_patient = None
                        st.session_state.page = "home"
                        st.rerun()


    cols = st.columns(3, gap="small")
    patients = all_patients()

    ############
    # sort
    ############

    movements = get_all_movements()

    df_movements = pd.DataFrame(
        movements,
        columns=[
            "MOVEMENT_ID",
            "PATIENT_ID",
            "DATETIME",
            "MOVEMENT_TYPE",
            "ROM_VALUE",
            "JERK_VALUE",
            "RISK_LEVEL"
        ]
    )

    search_text = st.text_input("Search patient by name or ID")

    patient_stats = {}

    for patient in patients:
        pid = patient[0]

        patient_movements = df_movements[df_movements["PATIENT_ID"] == pid]

        high_risk_count = (
            patient_movements["RISK_LEVEL"]
            .astype(str)
            .str.lower()
            .eq("high")
            .sum()
        )

        if len(patient_movements) > 0:
            latest_update = pd.to_datetime(
                patient_movements["DATETIME"],
                errors="coerce"
            ).max()
        else:
            latest_update = pd.Timestamp.min

        patient_stats[pid] = {
            "high_risk_count": high_risk_count,
            "latest_update": latest_update
        }

    if not patients:
        st.info("No patients found in the database")

    filtered_patients = []

    for patient in patients:
        patient_id_text = f"{patient[0]:04d}"
        patient_name = patient[1]

        if search_text:
            if (
                    search_text.lower() not in patient_name.lower()
                    and search_text not in patient_id_text
            ):
                continue

        filtered_patients.append(patient)

    filtered_patients = sorted(
        filtered_patients,
        key=lambda p: (
            patient_stats[p[0]]["high_risk_count"],
            patient_stats[p[0]]["latest_update"]
        ),
        reverse=True
    )

    if not filtered_patients:
        st.info("No matching patients found")

    for i, patient in enumerate(filtered_patients):

        patient_id = f"{patient[0]:04d}"
        name = patient[1]
        gender = patient[2]
        dob = patient[3]

        high_risk_count = patient_stats[patient[0]]["high_risk_count"]
        latest_update = patient_stats[patient[0]]["latest_update"]

        if high_risk_count > 0:
            risk_text = f"High Risk: {high_risk_count}"
            risk_color = "#f28b82"
        else:
            risk_text = "No High Risk"
            risk_color = "#8fd19e"

        if pd.isna(latest_update) or latest_update == pd.Timestamp.min:
            latest_update_text = "No movement data"
        else:
            latest_update_text = latest_update.strftime("%Y-%m-%d %H:%M")

        with cols[i % 3]:
            with st.container(key=f"st-select_patient_card_{patient[0]}"):
                img_col, info_col = st.columns([1, 2], vertical_alignment="center")

                with img_col:
                    img_path = Path(__file__).with_name("icon.png")

                    if not os.path.exists(img_path):
                        display_img = f"https://ui-avatars.com/api/?name={name}&background=dbe7f3&color=1f4e79&bold=true&size=128"
                    else:
                        display_img = img_path

                    st.markdown('<div class="patient-img">', unsafe_allow_html=True)
                    st.image(display_img, width="stretch")
                    st.markdown("</div>", unsafe_allow_html=True)

                with info_col:
                    st.markdown(f"""
                    <div class="patient-meta">
                        ID: {patient_id}<br>
                        Name: {name}<br>
                        Gender: {gender}<br>
                        DOB: {dob}<br>
                        Latest Update: {latest_update_text}<br>
                        <span style="
                            display:inline-block;
                            margin-top:6px;
                            padding:4px 10px;
                            border-radius:12px;
                            background:{risk_color};
                            color:white;
                            font-weight:600;
                        ">
                            {risk_text}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                if st.button("Select", key=f"sel_{patient[0]}", width="stretch"):
                    st.session_state.selected_patient = patient
                    st.session_state.page = "patient"
                    st.rerun()

    # for i, patient in enumerate(patients):
    #
    #     patient_id = f"{patient[0]:04d}"
    #     name = patient[1]
    #     gender = patient[2]
    #     dob = patient[3]
    #
    #     with cols[i % 3]:
    #         with st.container(key=f"st-select_patient_card{i}"):
    #             img_col, info_col = st.columns([1, 2], vertical_alignment="center")
    #
    #             with img_col:
    #                 img_path = Path(__file__).with_name('icon.png')
    #                 if not os.path.exists(img_path):
    #                     display_img = f"https://ui-avatars.com/api/?name={name}&background=dbe7f3&color=1f4e79&bold=true&size=128"
    #                 else:
    #                     display_img = img_path
    #
    #                 st.markdown('<div class="patient-img">', unsafe_allow_html=True)
    #                 st.image(display_img, width='stretch')
    #                 st.markdown('</div>', unsafe_allow_html=True)
    #
    #             with info_col:
    #                 st.markdown(f"""
    #                 <div class="patient-meta">
    #                     ID: {patient_id}<br>
    #                     Name: {name}<br>
    #                     Gender: {gender}<br>
    #                     DOB: {dob}<br>
    #                 </div>
    #             """, unsafe_allow_html=True)
    #
    #             if st.button("Select", key=f"sel_{i}", width='stretch'):
    #                 st.session_state.selected_patient = patient
    #                 st.session_state.page = "patient"
    #                 st.rerun()
