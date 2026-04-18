import streamlit as st
import os
from data import patients


AVATAR_DIR = "avatars"

def show():
    st.markdown('<div class="main-title">Rehabilitation Decision Support System</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Patient Selection</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(4, gap="large")

    for i, patient in enumerate(patients):
        with cols[i]:
            with st.container(border=True):
                img_col, info_col = st.columns([1.5, 1.5])

                with img_col:
                    img_path = f"{AVATAR_DIR}/{patient['id']}.png"
                    if not os.path.exists(img_path):
                        display_img = f"https://ui-avatars.com/api/?name={patient['initials']}&background=dbe7f3&color=1f4e79&bold=true&size=128"
                    else:
                        display_img = img_path

                    st.markdown('<div class="patient-img">', unsafe_allow_html=True)
                    st.image(display_img, width='stretch')
                    st.markdown('</div>', unsafe_allow_html=True)

                with info_col:
                    st.markdown(
                        f'<div class="name-text" style="white-space: nowrap;">{patient["name"]}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(f'<div class="id-text">ID: {patient["id"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="gender-text">{patient["gender"]}</div>', unsafe_allow_html=True)

                if st.button("Select", key=f"sel_{i}", width='stretch'):
                    st.session_state.selected_patient = patient
                    st.session_state.page = "report"
                    st.rerun()
