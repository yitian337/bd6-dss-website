import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from data import all_patients, get_all_movements
import os
from pathlib import Path
import base64

img_path = Path(__file__).with_name("doctor.png")

with open(img_path, "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode()

def show():
    patients = all_patients()
    movements = get_all_movements()

    df_patients = pd.DataFrame(
        patients,
        columns=["PATIENT_ID", "NAME", "GENDER", "DOB"]
    )

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

    # -----------------------------
    # Hero section
    # -----------------------------

    st.html(f"""
    <div style="
        background: linear-gradient(120deg, #eef5ff 0%, #f8fbff 100%);
        border-radius: 28px;
        padding: 30px 42px;
        margin-bottom: 24px;
        border: 1px solid #dbe7f3;

        display:flex;
        align-items:center;
        justify-content:flex-start;
        gap:16px;
    ">

        <!-- 左边文字 -->
        <div style="
            width:60%;
        ">

            <div style="
                color:#6b7a8c;
                font-size:14px;
                margin-bottom:8px;
            ">
                AI Rehabilitation Decision Support
            </div>

            <div style="
                color:#1f4e79;
                font-size:44px;
                font-weight:700;
                line-height:1.15;
                max-width:620px;
                margin-bottom:18px;
            ">
                Intelligent rehabilitation monitoring you can rely on
            </div>

            <div style="
                color:#6b7a8c;
                font-size:17px;
                max-width:650px;
                line-height:1.6;
                margin-bottom:24px;
            ">
                Track patient movement quality, rehabilitation risk, and progress using motion analysis data.
            </div>

            <!-- 按钮 -->
            <a href="/?page=select" target="_self" style="
                display:inline-block;
                background:#2f5b82;
                color:white;
                padding:12px 24px;
                border-radius:24px;
                font-size:15px;
                font-weight:600;
                text-decoration:none;
            ">
                View Patient List
            </a>

        </div>

        <!-- 右边医生图片 -->
        <img src="data:image/png;base64,{img_base64}"
            style="
                width:300px;
                border-radius:20px;
            ">

    </div>
    """)
    # -----------------------------
    # Summary statistics
    # -----------------------------

    total_patients = len(df_patients)
    total_movements = len(df_movements)

    if len(df_movements) > 0:
        latest_update = pd.to_datetime(df_movements["DATETIME"]).max()
        latest_update_text = latest_update.strftime("%Y-%m-%d %H:%M")
    else:
        latest_update_text = "No data"

    col1, col2, col3 = st.columns(3)

    high_risk_count = 0

    if len(df_movements) > 0:
        high_risk_count = (
            df_movements["RISK_LEVEL"]
            .astype(str)
            .str.lower()
            .eq("high")
            .sum()
        )

    metric_cards = [
        ("Total Patients", total_patients),
        ("High Risk Cases", high_risk_count),
        ("Latest Update", latest_update_text)
    ]

    for col, (label, value) in zip([col1, col2, col3], metric_cards):
        with col:
            st.markdown(f"""
                <div style="
                    background: #f8fbff;
                    border: 1px solid #dbe7f3;
                    border-radius: 18px;
                    padding: 24px;
                    text-align: center;
                    min-height: 120px;
                ">
                    <div style="
                        color: #6b7a8c;
                        font-size: 15px;
                        font-weight: 600;
                        margin-bottom: 12px;
                    ">
                        {label}
                    </div>
                    <div style="
                        color: #2f5b82;
                        font-size: 30px;
                        font-weight: 700;
                    ">
                        {value}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Charts
    # -----------------------------

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    chart1, chart2, chart3 = st.columns(3)

    with chart1:
        st.markdown("### Gender Distribution")

        if len(df_patients) > 0:

            gender_counts = df_patients["GENDER"].value_counts()

            colors = []

            for gender in gender_counts.index:
                if str(gender).upper() == "M":
                    colors.append("#a8d8ff")  # 浅蓝
                elif str(gender).upper() == "F":
                    colors.append("#ffd6e7")  # 浅粉
                else:
                    colors.append("#d9d9d9")

            fig, ax = plt.subplots(figsize=(4, 3))

            ax.pie(
                gender_counts,
                labels=gender_counts.index,
                autopct="%1.0f%%",
                startangle=90,
                colors=colors
            )

            ax.axis("equal")

            st.pyplot(fig)

        else:
            st.info("No patient data available")

    with chart2:
        st.markdown("### Age Distribution")

        if len(df_patients) > 0:
            today = pd.Timestamp.today()

            df_patients["DOB"] = pd.to_datetime(
                df_patients["DOB"],
                errors="coerce"
            )

            df_patients["Age"] = (
                today.year - df_patients["DOB"].dt.year
            )

            fig, ax = plt.subplots(figsize=(4, 3))
            ax.hist(df_patients["Age"].dropna(), bins=5)
            ax.set_xlabel("Age")
            ax.set_ylabel("Patients")
            st.pyplot(fig)
        else:
            st.info("No patient data available")

    with chart3:
        st.markdown("### Risk Distribution")

        if len(df_movements) > 0:
            risk_counts = df_movements["RISK_LEVEL"].value_counts()

            risk_colors = []

            for risk in risk_counts.index:
                risk_lower = str(risk).lower()

                if risk_lower == "low":
                    risk_colors.append("#8fd19e")  # 绿色
                elif risk_lower == "medium":
                    risk_colors.append("#ffe08a")  # 黄色
                elif risk_lower == "high":
                    risk_colors.append("#f28b82")  # 红色
                else:
                    risk_colors.append("#bdbdbd")

            fig, ax = plt.subplots(figsize=(4, 3))

            ax.bar(
                risk_counts.index,
                risk_counts.values,
                color=risk_colors
            )

            ax.set_xlabel("Risk Level")
            ax.set_ylabel("Movements")
            st.pyplot(fig)
        else:
            st.info("No movement data available")