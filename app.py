import streamlit as st
from styles import load_styles

load_styles()

# 初始化状态
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None

if "page" not in st.session_state:
    st.session_state.page = "select"

# 页面路由
if st.session_state.page == "select":
    import page1_patient_select
    page1_patient_select.show()

elif st.session_state.page == "report":
    import page2_report
    page2_report.show()

elif st.session_state.page == "details":
    import page3_details
    page3_details.show()