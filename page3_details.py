import os
import streamlit as st
from data import fake_reports

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resolve_local_path(rel_path):
    if not rel_path:
        return None
    if str(rel_path).startswith("http://") or str(rel_path).startswith("https://"):
        return rel_path
    return os.path.join(BASE_DIR, rel_path)

def show():
    patient = st.session_state.selected_patient

    # 默认 exercise
    if "selected_exercise" not in st.session_state:
        st.session_state.selected_exercise = "Reach and Retrieve"

    current_ex = st.session_state.selected_exercise
    report = fake_reports.get(current_ex, fake_reports["Unknown"])

    # =============================
    # Top area
    # =============================
    top_left, top_right = st.columns([6, 1])

    with top_left:
        st.markdown(
            '<div class="details-page-title">Patient Report</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="details-page-subtitle">{patient["name"]} | ID: {patient["id"]} | {patient.get("gender", "Unknown")}</div>',
            unsafe_allow_html=True
        )

    with top_right:
        if st.button("Back", key="details_back_btn", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================
    # Exercise categories
    # =============================
    st.markdown(
        '<div class="details-section-heading">Exercise Categories</div>',
        unsafe_allow_html=True
    )

    ex_cols = st.columns(4, gap="large")
    exercise_names = ["Reach and Retrieve", "Lift Arm", "Rotate Arm", "Unknown"]

    for idx, ex_name in enumerate(exercise_names):
        with ex_cols[idx]:
            is_active = current_ex == ex_name
            if st.button(
                ex_name,
                key=f"details_ex_btn_{idx}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.selected_exercise = ex_name
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # =============================
    # Image area
    # =============================
    st.markdown(
        f'<div class="details-section-heading" style="margin-top:10px;">{current_ex} Image</div>',
        unsafe_allow_html=True
    )

    image_path = report.get("image", "")
    full_image_path = resolve_local_path(image_path)

    with st.container(key="details_image_card"):
        if full_image_path and os.path.exists(full_image_path):
            st.image(full_image_path, use_container_width=True)
        else:
            st.markdown(
                """
                <div class="details-image-placeholder">
                    📷<br>
                    Image not found
                </div>
                """,
                unsafe_allow_html=True
            )