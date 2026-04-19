from pathlib import Path
import streamlit as st
import os
from data import all_patients, add_patient, max_id

BASE_DIR = Path(__file__).resolve().parent
AVATAR_DIR = BASE_DIR / "avatars"


def show():
    with st.popover("Add Patient"):
        with st.form("add_patient", clear_on_submit=True, enter_to_submit=False):
            np_name = st.text_input("Name")
            np_gender = st.text_input("Gender")
            np_age = st.text_input("Age")

            submit_btn = st.form_submit_button("Enter", width="stretch")

            if submit_btn:
                if np_name and np_gender and np_age:
                    raw_id = max_id() + 1
                    np_id = f"{raw_id:04d}"

                    add_patient(np_id, np_name, np_gender, np_age)
                    st.toast(f"Patient {np_name} added!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")

    st.markdown('<div class="main-title">Stroke Rehabilitation DSS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Patient Selection</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    patients = all_patients()
    cols = st.columns(4, gap="medium")

    if not patients:
        st.info("No patients found in the database")
        return

    for i, patient in enumerate(patients):
        patient_id = str(patient[0]).strip()
        name = patient[1]
        gender = patient[2]
        age = patient[3]

        with cols[i % 4]:
            with st.container(border=True):
                img_col, info_col = st.columns([1.5, 1.5], vertical_alignment="center")

                with img_col:
                    avatar_candidates = [
                        AVATAR_DIR / f"{patient_id}.png",
                        AVATAR_DIR / f"{patient_id}.jpg",
                        AVATAR_DIR / f"{patient_id}.jpeg",
                    ]

                    avatar_path = None
                    for path in avatar_candidates:
                        if path.exists():
                            avatar_path = path
                            break

                    icon_path = BASE_DIR / "icon.png"

                    if avatar_path:
                        display_img = avatar_path
                    elif icon_path.exists():
                        display_img = icon_path
                    else:
                        display_img = (
                            f"https://ui-avatars.com/api/"
                            f"?name={name}&background=dbe7f3&color=1f4e79&bold=true&size=128"
                        )

                    st.markdown('<div class="patient-img">', unsafe_allow_html=True)
                    st.image(display_img, width="stretch")
                    st.markdown('</div>', unsafe_allow_html=True)

                with info_col:
                    st.markdown(
                        f'<div class="name-text" style="white-space: nowrap;">{name}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(f'<div class="id-text">ID: {patient_id}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gender-text">Gender: {gender}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="age-text">Age: {age}</div>', unsafe_allow_html=True)

                if st.button("Select", key=f"sel_{i}", width="stretch"):
                    st.session_state.selected_patient = {
                        "id": patient_id,
                        "name": name,
                        "gender": gender,
                        "age": age,
                    }
                    st.session_state.page = "report"
                    st.rerun()