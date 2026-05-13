import os
from pathlib import Path
import streamlit as st
from data import *
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def show():
    patient = st.session_state.selected_patient

    patient_id = f"{patient[0]:04d}"
    name = patient[1]
    gender = patient[2]
    dob = patient[3]

    # -----------------------------
    # Top card
    # -----------------------------

    with st.container(key="st-patient_info_card"):

        left, middle, x, right = st.columns([2, 1, 1, 1], gap="medium")

        with left:
            icon, info = st.columns([1, 2], gap="medium", vertical_alignment="center")

            with icon:
                img_path = Path(__file__).with_name("icon.png")
                if not os.path.exists(img_path):
                    display_img = (
                        f"https://ui-avatars.com/api/?name={name}"
                        f"&background=dbe7f3&color=1f4e79&bold=true&size=128"
                    )
                else:
                    display_img = img_path

                st.markdown('<div class="patient-img">', unsafe_allow_html=True)
                st.image(display_img, width="content")
                st.markdown("</div>", unsafe_allow_html=True)

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
            st.markdown(
                '<div class="section-title">Patient Dashboard</div>',
                unsafe_allow_html=True
            )

        with right:
            with st.container(key="back_wrap"):
                if st.button("← Back", key="back_btn", use_container_width=True):
                    st.session_state.selected_patient = None
                    st.session_state.page = "select"
                    st.rerun()

            with st.container(key="report_wrap"):
                if st.button("View Reports", key="report_btn", use_container_width=True):
                    st.session_state.page = "report"
                    st.rerun()
            
            with st.popover("Load Data", use_container_width=True):
                st.markdown('<div class="section-title">Load New Data</div>', unsafe_allow_html=True)
                st.markdown('<div class="dropdown-label">Upload new movement data for this patient</div>', unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="data_upload")

    # -----------------------------
    # Prepare movement data
    # -----------------------------

    movements = get_patient_movements(patient[0])
    table_data = []

    for movement in movements:
        movement_id = movement[0]
        datetime_str = movement[1]
        movement_type = movement[2]
        rom_value = movement[3]
        jerk_value = movement[4]
        risk_level = movement[5]

        try:
            dt = datetime.fromisoformat(datetime_str)
            day = dt.strftime("%Y-%m-%d")
            time_str = dt.strftime("%H:%M:%S")
        except ValueError:
            day = datetime_str
            time_str = ""

        table_data.append({
            "Day": day,
            "Time": time_str,
            "Risk": risk_level,
            "Movement": movement_type,
            "ID": movement_id,
            "ROM": rom_value,
            "Jerk": jerk_value,
            "DatetimeRaw": datetime_str
        })

    df_summary = pd.DataFrame(table_data)

    if len(df_summary) > 0:
        avg_jerk = df_summary["Jerk"].mean()
        avg_rom = df_summary["ROM"].mean()
        total_movements = len(df_summary)

        risk_order = {"Low": 1, "Medium": 2, "High": 3}
        reverse_risk_order = {1: "Low", 2: "Medium", 3: "High"}

        avg_risk_num = df_summary["Risk"].map(risk_order).mean()
        avg_risk_text = reverse_risk_order.get(round(avg_risk_num), "N/A")

        movement_counts = df_summary["Movement"].value_counts()
    else:
        avg_jerk = 0
        avg_rom = 0
        total_movements = 0
        avg_risk_text = "N/A"
        movement_counts = pd.Series(dtype=int)

    left_col, graph_col, right_col = st.columns(
        [1, 2, 1],
        gap="medium",
        vertical_alignment="top"
    )

    # -----------------------------
    # Left metric cards
    # -----------------------------

    with left_col:
        left_metrics = {
            "Average Jerk Value": f"{avg_jerk:.3f}",
            "Average ROM": f"{avg_rom:.2f}",
            "Risk": avg_risk_text,
            "Total Movements": str(total_movements)
        }

        for i, (label, value) in enumerate(left_metrics.items()):
            with st.container(key=f"st-key-left_metric_{i}"):
                st.markdown(f"""
                    <div style="
                        background: #f8fbff;
                        border: 1px solid #dbe7f3;
                        border-radius: 14px;
                        padding: 16px;
                        min-height: 122px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        color: #6b7a8c;
                        font-size: 14px;
                        margin-bottom: 12px;
                    ">
                        <div style="font-weight: bold; margin-bottom: 8px;">{label}</div>
                        <div style="font-size: 25px; color: #2f5b82;">{value}</div>
                    </div>
                """, unsafe_allow_html=True)

    # -----------------------------
    # Graph card
    # -----------------------------

    with graph_col:
        st.markdown("""
            <style>
            .st-key-graph_card {
                background: #f8fbff;
                border: 1px solid #dbe7f3;
                border-radius: 14px;
                padding: 24px;
                min-height: 420px;
                margin-top: -20px;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.container(key="graph_card"):

            if len(df_summary) == 0:
                st.markdown("""
                    <div style="
                        min-height: 360px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: #6b7a8c;
                        font-size: 16px;
                    ">
                        No movement data available
                    </div>
                """, unsafe_allow_html=True)

            else:
                graph_type = st.session_state.get("metric_selector", "Risk")

                df_chart = pd.DataFrame(table_data)

                df_chart["Datetime"] = pd.to_datetime(
                    df_chart["DatetimeRaw"],
                    errors="coerce"
                )

                df_chart = df_chart.sort_values("Datetime").reset_index(drop=True)

                fig, ax = plt.subplots(figsize=(8, 4))

                if graph_type == "Risk":
                    risk_map = {
                        "Low": 1,
                        "Medium": 2,
                        "High": 3
                    }

                    df_chart["RiskValue"] = df_chart["Risk"].map(risk_map)

                    ax.axhspan(0.5, 1.5, color="green", alpha=0.18)
                    ax.axhspan(1.5, 2.5, color="yellow", alpha=0.18)
                    ax.axhspan(2.5, 3.5, color="red", alpha=0.18)

                    ax.plot(
                        df_chart["Datetime"],
                        df_chart["RiskValue"],
                        marker="o",
                        linewidth=2
                    )

                    ax.set_ylabel("Risk Level")
                    ax.set_ylim(0.5, 3.5)
                    ax.set_yticks([1, 2, 3])
                    ax.set_yticklabels(["Low", "Medium", "High"])

                    title = "Rehabilitation Risk Trend"

                    caption = (
                        "Higher risk levels may indicate reduced movement quality or "
                        "unstable rehabilitation performance."
                    )

                elif graph_type == "ROM":
                    df_chart["ROM_smooth"] = (
                        df_chart["ROM"]
                        .rolling(window=10, min_periods=1)
                        .mean()
                    )

                    ax.plot(
                        df_chart["Datetime"],
                        df_chart["ROM_smooth"],
                        linewidth=2
                    )

                    ax.set_ylabel("ROM Value")

                    title = "Range of Motion (ROM) Over Time"

                    caption = (
                        "Higher ROM values generally indicate better movement range "
                        "during rehabilitation exercises."
                    )

                else:
                    df_chart["Jerk_smooth"] = (
                        df_chart["Jerk"]
                        .rolling(window=10, min_periods=1)
                        .mean()
                    )

                    ax.plot(
                        df_chart["Datetime"],
                        df_chart["Jerk_smooth"],
                        linewidth=2
                    )

                    ax.set_ylabel("Jerk Value")

                    title = "Movement Smoothness (Jerk) Over Time"

                    caption = (
                        "Lower jerk values generally indicate smoother and more stable "
                        "rehabilitation movement."
                    )

                ax.set_xlabel("Time")
                plt.xticks(rotation=45)
                plt.tight_layout()

                st.markdown(f"""
                    <div style="
                        text-align: center;
                        color: #2f5b82;
                        font-size: 24px;
                        font-weight: 600;
                        margin-bottom: 10px;
                    ">
                        {title}
                    </div>
                """, unsafe_allow_html=True)

                st.pyplot(fig)

                st.caption(caption)

                st.markdown("<br>", unsafe_allow_html=True)

                st.selectbox(
                    "Select Metric",
                    ["Risk", "ROM", "Jerk"],
                    key="metric_selector"
                )

    # -----------------------------
    # Right metric cards
    # -----------------------------

    with right_col:
        right_metrics = {
            "Reach & Retrieve Repetitions": movement_counts.get("A", 0),
            "Cup to Mouth Repetitions": movement_counts.get("B", 0),
            "Swing Arm Repetitions": movement_counts.get("C", 0),
            "Rotate Wrist Repetitions": movement_counts.get("D", 0)
        }

        for i, (label, value) in enumerate(right_metrics.items()):
            with st.container(key=f"st-key-right_metric_{i}"):
                st.markdown(f"""
                    <div style="
                        background: #f8fbff;
                        border: 1px solid #dbe7f3;
                        border-radius: 14px;
                        padding: 16px;
                        min-height: 121px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        color: #6b7a8c;
                        font-size: 14px;
                        margin-bottom: 12px;
                    ">
                        <div style="font-weight: bold; margin-bottom: 8px;">{label}</div>
                        <div style="font-size: 25px; color: #2f5b82;">{value}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Notes section
    # -----------------------------

    with st.container(key="st-key-notes_card"):
        st.markdown('<div class="section-title">Notes</div>', unsafe_allow_html=True)

        notes_text = st.text_area(
            "Patient Notes",
            placeholder="Enter clinical notes here...",
            height=120,
            label_visibility="collapsed",
            max_chars=600
        )

        col1, col2 = st.columns([4, 1], gap="medium")

        with col2:
            if st.button("Save Note", use_container_width=True):
                if notes_text.strip():
                    datetime_str = datetime.now().isoformat()
                    add_note(patient[0], datetime_str, notes_text)
                    st.success("Note saved successfully!")
                    st.rerun()
                else:
                    st.warning("Please enter a note before saving.")