import streamlit as st
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from data import *


def show():
    st.markdown('<div class="main-title">Stroke Monitoring System</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Button at the top
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
    with col_btn2:
        if st.button("Patient Menu", key="back_btn", use_container_width=True):
            st.session_state.page = "select"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Get patient statistics
    patients = all_patients()
    
    if patients:
        total_patients = len(patients)
        
        # Display total patients stat
        st.markdown(f'<div class="section-title">Total Patients: {total_patients}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display graphs side by side
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.subheader("Patient Demographics")
            
            # Calculate ages from DOB
            ages = []
            for patient in patients:
                dob_str = patient[3]
                try:
                    dob = datetime.strptime(dob_str, "%Y-%m-%d")
                    today = datetime.now()
                    age = (today - dob).days // 365
                    ages.append(age)
                except (ValueError, TypeError):
                    pass
            
            if ages:
                fig, ax = plt.subplots(figsize=(5, 3))
                ax.hist(ages, bins=10, color="#2f5b82", edgecolor="white", linewidth=1.2)
                ax.set_xlabel("Age (years)", fontsize=9)
                ax.set_ylabel("Count", fontsize=9)
                ax.grid(axis="y", alpha=0.2, linestyle="--")
                ax.set_facecolor("#f8fbff")
                fig.patch.set_facecolor("white")
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
            else:
                st.info("No valid patient dates of birth available.")
        
        with col2:
            st.subheader("Overall Patient Risk")
            all_movements = get_all_movements()
            
            if all_movements:
                risk_counts = {"High": 0, "Medium": 0, "Low": 0}
                for movement in all_movements:
                    risk_level = movement[4]
                    if risk_level in risk_counts:
                        risk_counts[risk_level] += 1
                
                fig, ax = plt.subplots(figsize=(5, 3))
                colors = ["#d32f2f", "#f57c00", "#388e3c"]
                bars = ax.bar(risk_counts.keys(), risk_counts.values(), color=colors, edgecolor="white", linewidth=1.2)
                ax.set_ylabel("Movements", fontsize=9)
                ax.grid(axis="y", alpha=0.2, linestyle="--")
                ax.set_facecolor("#f8fbff")
                fig.patch.set_facecolor("white")
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontsize=9, fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)
            else:
                st.info("No movement data available")
    else:
        st.info("No patients in the system yet.")