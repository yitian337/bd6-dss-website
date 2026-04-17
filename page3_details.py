import streamlit as st

def show():
    patient = st.session_state.selected_patient

    st.markdown(f"## Patient Details")
    st.markdown(f"### {patient['name']}")
    st.write(f"ID: {patient['id']}")
    st.write(f"Gender: {patient.get('gender', 'Unknown')}")
    st.write(f"Age: {patient.get('age', 'N/A')}")

    if st.button("← Back to Report", key="details_back_btn"):
        st.session_state.page = "report"
        st.rerun()