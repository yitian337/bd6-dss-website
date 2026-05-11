import os
from pathlib import Path
import streamlit as st
from data import *
import time


def show():
    patient = st.session_state.selected_patient
    
    patient_id = f"{patient[0]:04d}"
    name = patient[1]
    gender = patient[2]
    dob = patient[3]

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
                        DOB: {dob}<br>
                    </div>
                """, unsafe_allow_html=True)
        
        with middle:
            st.markdown('<div class="section-title">Patient Dashboard</div>', unsafe_allow_html=True)

        with right:
            with st.container(key="back_wrap"):
                if st.button("← Back", key="back_btn", use_container_width=True):
                    st.session_state.selected_patient = None
                    st.session_state.page = "select"
                    st.rerun()
            
            with st.container(key="report_wrap"):
                if st.button("View Reports", key="report_btn", use_container_width=True):
                    st.session_state.page = "patient"
                    st.session_state.page = "report"
                    st.rerun()

    # # -----------------------------
    # # Main content area
    # # -----------------------------

    left_col, graph_col, right_col = st.columns([1, 2, 1], gap="medium", vertical_alignment="top")

    with left_col:
        left_labels = ["Average Jerk Value", "Average ROM", "Average Risk Value", "Total Movements"]
        for i, label in enumerate(left_labels):
            with st.container(key=f"st-key-left_metric_{i}"):
                st.markdown(f"""
                    <div style="
                        background: #f8fbff;
                        border: 1px solid #dbe7f3;
                        border-radius: 14px;
                        padding: 16px;
                        min-height: 96px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        color: #6b7a8c;
                        font-size: 14px;
                        margin-bottom: 12px;
                    ">
                        <div style="font-weight: bold; margin-bottom: 8px;">{label}</div>
                        <div style="font-size: 18px; color: #2f5b82;">--</div>
                    </div>
                """, unsafe_allow_html=True)

    with graph_col:
        with st.container(key="st-key-graph_card"):
            st.markdown("""
                <div style="
                    background: #f8fbff;
                    border: 1px solid #dbe7f3;
                    border-radius: 14px;
                    padding: 24px;
                    min-height: 420px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #6b7a8c;
                    font-size: 16px;
                    text-align: center;
                ">
                    Graph Placeholder
                </div>
            """, unsafe_allow_html=True)

    with right_col:
        right_labels = ["Reach & Retrieve Repetitions", "Cup to Mouth Repetitions", "Lift Arm Repetitions", "Rotate Arm Repetitions"]
        for i, label in enumerate(right_labels):
            with st.container(key=f"st-key-right_metric_{i}"):
                st.markdown(f"""
                    <div style="
                        background: #f8fbff;
                        border: 1px solid #dbe7f3;
                        border-radius: 14px;
                        padding: 16px;
                        min-height: 96px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        color: #6b7a8c;
                        font-size: 14px;
                        margin-bottom: 12px;
                    ">
                        <div style="font-weight: bold; margin-bottom: 8px;">{label}</div>
                        <div style="font-size: 18px; color: #2f5b82;">--</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # # -----------------------------
    # # Notes section
    # # -----------------------------

    with st.container(key="st-key-notes_card"):
        st.markdown('<div class="section-title">Notes</div>', unsafe_allow_html=True)
        notes_text = st.text_area("Patient Notes", placeholder="Enter clinical notes here...", height=120, label_visibility="collapsed")




    # with st.container(key="top_card"):
    #     col1, col2 = st.columns([9, 1], gap="large")

    #     with col1:
    #         av, info = st.columns([1.2, 6], gap="medium")

    #         with av:
    #             st.markdown(
    #                 """
    #                 <div style="
    #                     width:90px;
    #                     height:90px;
    #                     border-radius:18px;
    #                     background:#eef5fb;
    #                     border:1px dashed #c5d6ea;
    #                     display:flex;
    #                     align-items:center;
    #                     justify-content:center;
    #                     flex-direction:column;
    #                     font-size:12px;
    #                     color:#6b7a8c;
    #                     text-align:center;
    #                 ">
    #                     Image<br>not found
    #                 </div>
    #                 """,
    #                 unsafe_allow_html=True
    #             )

    #         with info:
    #             st.markdown(f"""
    #                 <div class="patient-name">{patient["name"]}</div>
    #                 <div class="patient-meta">
    #                     ID: {patient["id"]}<br>
    #                     Gender: {patient.get("gender", "Unknown")}<br>
    #                     Age: {patient.get("age", "N/A")}<br>
    #                     Latest Session: 2026-04-17
    #                 </div>
    #             """, unsafe_allow_html=True)

    #     with col2:
    #         with st.container(key="back_wrap"):
    #             if st.button("← Back", key="back_btn", use_container_width=True):
    #                 st.session_state.selected_patient = None
    #                 st.session_state.page = "select"
    #                 st.rerun()
    #             if st.button("Details", key="details_btn", use_container_width=True):
    #                 st.session_state.page = "details"
    #                 st.rerun()
    
    # # -----------------------------
    # # Reports
    # # -----------------------------

    # report = fake_reports.get(patient["name"])
    # if report is None:
    #     st.warning("No report found")
    #     st.stop()
    # patient_id = patient["id"]

    # # ==================== 三栏布局 ====================
    # left, main, right = st.columns([1.2, 5.5, 1.1], gap="small", vertical_alignment="top")

    # # Left Sidebar
    # with left:
    #     with st.container(key="sidebar_card"):
    #         st.markdown('<div class="section-title">Patients</div>', unsafe_allow_html=True)
    #         st.markdown(
    #             '<div class="dropdown-label">Select a patient to switch report view</div>',
    #             unsafe_allow_html=True
    #         )

    #         patient_labels = [f'{p["name"]} ({p["id"]})' for p in patients]
    #         current_index = next(
    #             (i for i, p in enumerate(patients) if p["id"] == patient["id"]),
    #             0
    #         )

    #         selected_label = st.radio(
    #             "Patient list",
    #             patient_labels,
    #             index=current_index,
    #             label_visibility="collapsed"
    #         )

    #         selected_patient = patients[patient_labels.index(selected_label)]

    #         if selected_patient["id"] != patient["id"]:
    #             st.session_state.selected_patient = selected_patient
    #             st.rerun()