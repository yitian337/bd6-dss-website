import streamlit as st
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    else:
        st.info("No patients in the system yet.")
    
    # # -----------------------------
    # # Patient statistics section
    # # -----------------------------