import streamlit as st
from styles import load_styles
from data import *

init_data()
load_styles()

# initialise page
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None

if "page" not in st.session_state:
    st.session_state.page = "home"

# read page from URL only once, then clear it
query_page = st.query_params.get("page")

if query_page:
    st.session_state.page = query_page
    st.query_params.clear()

# open page
if st.session_state.page == "home":
    import page_home
    page_home.show()

elif st.session_state.page == "select":
    import page_select
    page_select.show()

elif st.session_state.page == "patient":
    import page_patient
    page_patient.show()

elif st.session_state.page == "report":
    import page_report
    page_report.show()