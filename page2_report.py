import os
import streamlit as st
from data import patients, fake_reports
import time

#get photo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_avatar_path(patient_id):
    return os.path.join(BASE_DIR, "avatars", f"{patient_id}.png")


def show():
    patient = st.session_state.selected_patient
    report = fake_reports.get(patient["name"])
    if report is None:
        st.warning("No report found")
        st.stop()
    patient_id = patient["id"]

    avatar_path = get_avatar_path(patient_id)

    # ==================== Top Card ====================
    with st.container(key="top_card"):
        col1, col2 = st.columns([9, 1], gap="large")

        with col1:
            av, info = st.columns([0.8, 6], gap="medium")

            with av:
                avatar_path = get_avatar_path(str(patient["id"]).strip())

                if os.path.exists(avatar_path):
                    st.markdown('<div style="margin-left:-10px; margin-top:10px;">', unsafe_allow_html=True)
                    st.image(avatar_path, width=90)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        """
                        <div style="
                            width:90px;
                            height:90px;
                            border-radius:18px;
                            background:#eef5fb;
                            border:1px dashed #c5d6ea;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            flex-direction:column;
                            font-size:12px;
                            color:#6b7a8c;
                            text-align:center;
                        ">
                            Image<br>not found
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with info:
                st.markdown(f"""
                    <div class="patient-name">{patient["name"]}</div>
                    <div class="patient-meta">
                        ID: {patient["id"]}<br>
                        Gender: {patient.get("gender", "Unknown")}<br>
                        Age: {patient.get("age", "N/A")}<br>
                        Latest Session: 2026-04-17
                    </div>
                """, unsafe_allow_html=True)

        with col2:
            with st.container(key="back_wrap"):
                if st.button("← Back", key="back_btn", use_container_width=True):
                    st.session_state.selected_patient = None
                    st.session_state.page = "select"
                    st.rerun()
                if st.button("Details", key="details_btn", use_container_width=True):
                    st.session_state.page = "details"
                    st.rerun()

    # ==================== 三栏布局 ====================
    left, main, right = st.columns([1.2, 5.5, 1.1], gap="small", vertical_alignment="top")

    # Left Sidebar
    with left:
        with st.container(key="sidebar_card"):
            st.markdown('<div class="section-title">Patients</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="dropdown-label">Select a patient to switch report view</div>',
                unsafe_allow_html=True
            )

            patient_labels = [f'{p["name"]} ({p["id"]})' for p in patients]
            current_index = next(
                (i for i, p in enumerate(patients) if p["id"] == patient["id"]),
                0
            )

            selected_label = st.radio(
                "Patient list",
                patient_labels,
                index=current_index,
                label_visibility="collapsed"
            )

            selected_patient = patients[patient_labels.index(selected_label)]

            if selected_patient["id"] != patient["id"]:
                st.session_state.selected_patient = selected_patient
                st.rerun()

    # Main Area
    with main:
        with st.container(key="main_card"):
            st.markdown('<div class="section-title">Session Recording Analysis</div>', unsafe_allow_html=True)

            # update image here
            st.markdown(
                """
                <div style="
                    width:100%;
                    height:300px;
                    border-radius:18px;
                    background:#eef5fb;
                    border:1px dashed #c5d6ea;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    flex-direction:column;
                    font-size:14px;
                    color:#6b7a8c;
                    text-align:center;
                ">
                    📷<br>
                    Image not found
                </div>
                """,
                unsafe_allow_html=True
            )

    # Right Metrics
    with right:
        st.markdown(
            '<div class="report-section-title" style="visibility:hidden;">Metrics</div>',
            unsafe_allow_html=True
        )

        metrics = [
            ("Overall Score", "score"),
            ("ROM", "rom"),
            ("Stability", "stability"),
            ("Coordination", "coordination"),
        ]

        for i, (label, key_name) in enumerate(metrics):
            with st.container(key=f"metric_card_{i}"):
                st.markdown(f'<div class="metric-label">{label}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{report.get(key_name, "N/A")}</div>', unsafe_allow_html=True)

    # Summary
    with st.container(key="summary_card"):
        st.markdown('<div class="section-title">Clinical Summary</div>', unsafe_allow_html=True)

        st.markdown(
            f"""

            <div class="summary-block">
                <div class="summary-label">AI Feedback</div>
                <div class="summary-value">{report.get("feedback", "")}</div>
            </div>

            """,
            unsafe_allow_html=True
        )

        # Clinician Note
        st.markdown(
            '<div class="summary-label">Clinician Note</div>',
            unsafe_allow_html=True
        )

        note = st.text_area(
            "Edit clinician note",
            value=report.get("clinician_note", ""),
            key=f"note_{patient['id']}",
            height=120,
            label_visibility="collapsed"
        )

        msg = st.empty()

        if st.button("Save Note"):
            fake_reports[patient["name"]]["clinician_note"] = note
            msg.success("Saved!")
            time.sleep(2)
            msg.empty()