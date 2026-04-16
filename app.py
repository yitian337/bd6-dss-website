import streamlit as st
import pandas as pd

st.set_page_config(page_title="BD6 DSS", layout="wide")

st.title("Stroke Rehabilitation DSS")
st.write("This is a simple DSS prototype for physiotherapists.")

patients = ["Patient A", "Patient B", "Patient C"]
selected_patient = st.sidebar.selectbox("Select patient", patients)

st.subheader(f"Patient Overview: {selected_patient}")

movement_data = pd.DataFrame({
    "Movement": ["Reach & Retrieve", "Lift Cup", "Swing Arm", "Wrist Rotate"],
    "Count": [12, 8, 15, 10]
})

col1, col2 = st.columns(2)

with col1:
    st.write("### Movement Counts")
    st.bar_chart(movement_data.set_index("Movement"))

with col2:
    st.write("### Movement Quality")
    st.metric("Smooth movements", "80%")
    st.metric("Jerky movements", "20%")

st.write("### Daily Notes")
st.info("Patient completed most prescribed movements today.")