import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="BD6 DSS", layout="wide")

# initialize
if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None

if "selected_movement" not in st.session_state:
    st.session_state.selected_movement = "Reach and Retrieve"


# page1, choose patient
if st.session_state.page == "home":

    st.title("Stroke Rehabilitation DSS")
    st.header("Select Patient")

    patients = ["Patient A", "Patient B", "Patient C"]

    selected = st.selectbox("Choose a patient:", patients)

    if st.button("Enter Dashboard"):
        st.session_state.selected_patient = selected
        st.session_state.page = "dashboard"
        st.rerun()


#page2, Dashboard
elif st.session_state.page == "dashboard":

    patient = st.session_state.selected_patient
    st.title(f"{patient} Dashboard")

    if st.button("← Back to Patient Selection"):
        st.session_state.page = "home"
        st.rerun()

    st.subheader("Select Movement Type")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Reach and Retrieve"):
            st.session_state.selected_movement = "Reach and Retrieve"

    with col2:
        if st.button("Lift Arm"):
            st.session_state.selected_movement = "Lift Arm"

    with col3:
        if st.button("Rotate Arm"):
            st.session_state.selected_movement = "Rotate Arm"

    with col4:
        if st.button("Unknown"):
            st.session_state.selected_movement = "Unknown"

    movement = st.session_state.selected_movement

    st.subheader(f"Current Movement: {movement}")

    # data
    np.random.seed(len(movement))

    movement_count = np.random.randint(5, 20)
    smooth_percent = np.random.randint(60, 95)
    jerky_percent = 100 - smooth_percent

    trace_data = np.cumsum(np.random.randn(30))

    # indicators
    c1, c2, c3 = st.columns(3)

    c1.metric("Movement Count", movement_count)
    c2.metric("Smooth", f"{smooth_percent}%")
    c3.metric("Jerky", f"{jerky_percent}%")

    # graphs
    st.subheader("Movement Trace Graph")

    trace_df = pd.DataFrame({
        "Trace": trace_data
    })

    st.line_chart(trace_df)