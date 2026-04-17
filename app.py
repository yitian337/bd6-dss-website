import streamlit as st
import os
import random

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# Page Styles
# -----------------------------
st.markdown("""
<style>
/* page 1 */
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
    color: #1f4e79;
    margin-top: 10px;
    margin-bottom: 8px;
}

.section-title {
    text-align: center;
    font-size: 22px;
    font-weight: 600;
    color: #3d3d3d;
    margin-bottom: 40px;
}

.block-container {
    max-width: 1200px; 
    padding-top: 2rem;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #f8fbff;
    border: 1px solid #dbe7f3 !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    min-height: 250px;
}

.name-text {
    font-size: 20px;
    font-weight: 800;
    color: #1f1f1f;
    margin-bottom: 2px;
}

.id-text {
    font-size: 15px;
    color: #5f6b7a;
    margin-bottom: 15px;
}

.gender-text {
    font-size: 14px;
    color: #8a96a3;
}

.patient-img img {
    border-radius: 10px;
    object-fit: cover;
}

div.stButton > button:first-child {
    background-color: #1f4e79;
    color: white;
    border-radius: 10px;
    border: none;
    height: 45px;
    font-weight: 600;
    margin-top: 15px;
}

div.stButton > button:hover {
    background-color: #163657;
    color: white;
}

[data-testid="column"] {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}

/* page 2 */
.report-title {
    font-size: 32px;
    font-weight: 700;
    color: #1f4e79;
    margin-bottom: 6px;
}

.report-subtitle {
    font-size: 18px;
    color: #5f6b7a;
    margin-bottom: 24px;
}

.metric-card {
    background-color: #eef5fb;
    border: 1px solid #dbe7f3;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
}

.metric-label {
    font-size: 14px;
    color: #6b7a8c;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #1f4e79;
}

.action-header {
    font-size: 20px;
    font-weight: 700;
    color: #1f1f1f;
    margin-bottom: 12px;
}

.info-box {
    background-color: #f8fbff;
    border: 1px solid #dbe7f3;
    border-radius: 14px;
    padding: 18px;
    margin-top: 20px;
}

.small-label {
    color: #6b7a8c;
    font-size: 14px;
    margin-bottom: 4px;
}

.small-value {
    color: #1f1f1f;
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 12px;
}

.back-button div.stButton > button:first-child {
    background-color: #6c7a89;
}

.back-button div.stButton > button:hover {
    background-color: #4f5b67;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Data & Setup
# later can be replaced by SQL
# -----------------------------
patients = [
    {"id": "P001", "name": "Patient A", "gender": "Unknown", "initials": "PA"},
    {"id": "P002", "name": "Patient B", "gender": "Unknown", "initials": "PB"},
    {"id": "P003", "name": "Patient C", "gender": "Unknown", "initials": "PC"},
    {"id": "P004", "name": "Patient D", "gender": "Unknown", "initials": "PD"},
]

AVATAR_DIR = "avatars"

# -----------------------------
# Fake exercise report data
# later can be replaced by SQL
# -----------------------------
fake_reports = {
    "Reach and Retrieve": {
        "score": 84,
        "rom": "72%",
        "stability": "80%",
        "coordination": "78%",
        "feedback": "The patient completed the reach task with moderate control. Slight trunk compensation was observed during forward reach.",
        "clinician_note": "Encourage slower reaching speed and reduce shoulder elevation during retrieval.",
        "image": "images/reach.png"
    },
    "Lift Arm": {
        "score": 88,
        "rom": "85%",
        "stability": "82%",
        "coordination": "86%",
        "feedback": "Arm lifting performance was generally good. Minor asymmetry appeared near the end of the movement.",
        "clinician_note": "Continue with guided repetition and monitor fatigue in the final phase.",
        "image": "images/lift_arm.png"
    },
    "Rotate Arm": {
        "score": 76,
        "rom": "68%",
        "stability": "74%",
        "coordination": "71%",
        "feedback": "Rotation task showed limited range and reduced smoothness. Compensation at the shoulder was detected.",
        "clinician_note": "Focus on controlled rotation and reduce excessive upper body movement.",
        "image": "images/rotate_arm.png"
    },
    "Unknown": {
        "score": 69,
        "rom": "61%",
        "stability": "65%",
        "coordination": "63%",
        "feedback": "Unknown exercise category. Motion quality appears inconsistent and requires manual review.",
        "clinician_note": "Please verify exercise type and confirm whether the uploaded sample is correctly labeled.",
        "image": "images/unknown.png"
    }
}

# -----------------------------
# Session state init
# -----------------------------
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None

if "selected_exercise" not in st.session_state:
    st.session_state.selected_exercise = "Reach and Retrieve"

# -----------------------------
# Page 1: Patient selection
# -----------------------------
if st.session_state.selected_patient is None:
    st.markdown('<div class="main-title">Rehabilitation Decision Support System</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Patient Selection</div>', unsafe_allow_html=True)

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
                    st.session_state.selected_exercise = "Reach and Retrieve"
                    st.rerun()

# -----------------------------
# Page 2: Patient report page
# -----------------------------
else:
    patient = st.session_state.selected_patient

    top_left, top_right = st.columns([6, 1])

    with top_left:
        st.markdown('<div class="report-title">Patient Report</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="report-subtitle">{patient["name"]} | ID: {patient["id"]} | {patient["gender"]}</div>',
            unsafe_allow_html=True
        )

    with top_right:
        st.markdown('<div class="back-button">', unsafe_allow_html=True)
        if st.button("Back", key="back_btn", width='stretch'):
            st.session_state.selected_patient = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="action-header">Exercise Categories</div>', unsafe_allow_html=True)

    exercise_cols = st.columns(4, gap="medium")
    exercise_names = ["Reach and Retrieve", "Lift Arm", "Rotate Arm", "Unknown"]

    for idx, ex_name in enumerate(exercise_names):
        with exercise_cols[idx]:
            is_active = st.session_state.selected_exercise == ex_name
            button_type = "primary" if is_active else "secondary"

            if st.button(
                ex_name,
                key=f"ex_btn_{idx}",
                width='stretch',
                type=button_type
            ):
                st.session_state.selected_exercise = ex_name
                st.rerun()

    current_ex = st.session_state.selected_exercise
    report = fake_reports.get(current_ex, fake_reports["Unknown"])

    st.markdown("---")

    left_col, right_col = st.columns([2.2, 1.2], gap="large")

    with left_col:
        image_path = report["image"]

        # 显示图片：如果是本地文件则先检查是否存在
        if isinstance(image_path, str) and (
            image_path.startswith("http://") or image_path.startswith("https://")
        ):
            st.image(
                image_path,
                width='stretch',
                caption=f"Session Recording Analysis: {current_ex}"
            )
        else:
            if os.path.exists(image_path):
                st.image(
                    image_path,
                    width='stretch',
                    caption=f"Session Recording Analysis: {current_ex}"
                )
            else:
                st.warning(f"Image not found: {image_path}")

        st.markdown(
            f"""<div class="info-box">
<div class="small-label">Exercise Type</div>
<div class="small-value">{current_ex}</div>

<div class="small-label">Automated AI Feedback</div>
<div class="small-value">{report["feedback"]}</div>

<div class="small-label">Clinician Suggestion</div>
<div class="small-value">{report["clinician_note"]}</div>
</div>""",
            unsafe_allow_html=True
        )

    with right_col:
        m1, m2 = st.columns(2)

        with m1:
            st.markdown(
                f"""<div class="metric-card">
<div class="metric-label">Overall Score</div>
<div class="metric-value">{report["score"]}</div>
</div>""",
                unsafe_allow_html=True
            )

        with m2:
            st.markdown(
                f"""<div class="metric-card">
<div class="metric-label">ROM</div>
<div class="metric-value">{report["rom"]}</div>
</div>""",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        m3, m4 = st.columns(2)

        with m3:
            st.markdown(
                f"""<div class="metric-card">
<div class="metric-label">Stability</div>
<div class="metric-value">{report["stability"]}</div>
</div>""",
                unsafe_allow_html=True
            )

        with m4:
            st.markdown(
                f"""<div class="metric-card">
<div class="metric-label">Coordination</div>
<div class="metric-value">{report["coordination"]}</div>
</div>""",
                unsafe_allow_html=True
            )

        risk_level = random.choice(["Low", "Moderate"])

        st.markdown(
            f"""<div class="info-box">
<div class="small-label">Last Updated</div>
<div class="small-value">2026-04-17</div>

<div class="small-label">Session Risk Level</div>
<div class="small-value">{risk_level}</div>
</div>""",
            unsafe_allow_html=True
        )