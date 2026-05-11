from pathlib import Path
import streamlit as st
import os
from datetime import datetime
from data import *


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


    cols = st.columns(3, gap="medium")
    patients = all_patients()

    if not patients:
        st.info("No patients found in the database")

    for i, patient in enumerate(patients):

        patient_id = f"{patient[0]:04d}"
        name = patient[1]
        gender = patient[2]
        dob = patient[3]

        with cols[i % 3]:
            with st.container(key=f"st-select_patient_card{i}"):
                img_col, info_col = st.columns([1, 2], vertical_alignment="center")

                with img_col:
                    img_path = Path(__file__).with_name('icon.png')
                    if not os.path.exists(img_path):
                        display_img = f"https://ui-avatars.com/api/?name={name}&background=dbe7f3&color=1f4e79&bold=true&size=128"
                    else:
                        display_img = img_path

                    st.markdown('<div class="patient-img">', unsafe_allow_html=True)
                    st.image(display_img, width='stretch')
                    st.markdown('</div>', unsafe_allow_html=True)

                with info_col:
                    st.markdown(f"""
                    <div class="patient-meta">
                        ID: {patient_id}<br>
                        Name: {name}<br>
                        Gender: {gender}<br>
                        DOB: {dob}<br>
                    </div>
                """, unsafe_allow_html=True)

                if st.button("Select", key=f"sel_{i}", width='stretch'):
                    st.session_state.selected_patient = patient
                    st.session_state.page = "patient"
                    st.rerun()
