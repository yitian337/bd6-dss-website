import streamlit as st

st.set_page_config(layout="wide")

def load_styles():
    st.markdown("""
    <style>
    header {
        background-color: transparent !important;
    }

    .block-container {
        max-width: 1400px; 
        padding-top: 1rem;
    }
    
    .block-container {
        max-width: 1400px;
        padding-left: 50px;
        padding-right: 50px;
    }
    
    /* 通用文字 */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1f4e79;
        margin-bottom: 14px;
        text-align: center;
    }
    
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: #1f4e79;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .patient-name {
        font-size: 28px;
        font-weight: 700;
        color: #1f4e79;
        margin-bottom: 8px;
    }

    .patient-meta {
        font-size: 15px;
        color: #5f6b7a;
        line-height: 1.8;
        margin-bottom: 15px;
    }

    .patient-item-name {
        font-size: 15px;
        font-weight: 700;
        color: #1f1f1f;
        margin-bottom: 4px;
    }

    .patient-item-id {
        font-size: 13px;
        color: #6b7a8c;
    }

    .metric-label {
        font-size: 14px;
        color: #6b7a8c;
        margin-bottom: 8px;
        text-align: center;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #1f4e79;
        text-align: center;
    }

    .summary-label {
        color: #6b7a8c;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .summary-value {
        color: #1f1f1f;
        font-size: 15px;
        font-weight: 500;
        line-height: 1.7;
    }
                
    div[class*="st-select_patient_card"] {
        background: #f8fbff;
        border: 1px solid #dbe7f3;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 25px;
        min-height: 240px;
    }
                
    div[class*="st-patient_info_card"] {
        background: #f8fbff;
        border: 1px solid #dbe7f3;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 25px;
        max-height: 200px;
    }
                

    /* 顶部卡片 */
    .st-key-top_card {
        background: #f8fbff;
        border: 1px solid #dbe7f3;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 25px;
        min-height: 200px;
    }

    /* 左侧 sidebar */
    .st-key-sidebar_card {
        background: #f8fbff;
        border: 1px solid #dbe7f3;
        border-radius: 20px;
        padding: 20px;
        min-height: 540px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    /* 中间主卡片 */
    .st-key-main_card {
        background: #f8fbff;
        border: 1px solid #dbe7f3;
        border-radius: 20px;
        padding: 20px;
        min-height: 540px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    /* summary 外层 */
    .st-key-summary_card {
        background: #f8fbff;
        border: 1px solid #dbe7f3;
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    
    .summary-block {
        margin-bottom: 18px;
    }
    
    .summary-label {
        color: #6b7a8c;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    
    .summary-value {
        color: #1f1f1f;
        font-size: 15px;
        font-weight: 500;
        line-height: 1.8;
    }

    /* 左侧 patient item */
    div[class*="st-key-patient_item_"] {
        background: white;
        border: 1px solid #dbe7f3;
        border-radius: 14px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }

    div[class*="st-key-patient_item_active_"] {
        background: #eaf3ff;
        border: 1px solid #9fc4ea;
    }

    /* 右侧 metric card */
    div[class*="st-key-metric_card_"] {
        background: #eef5fb;
        border: 1px solid #dbe7f3;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        margin-bottom: 10px;
        min-height: 110px;
    }
    
    .report-section-title {
        text-align: center;
        font-size: 0px;
        font-weight: 0;
        color: #1f4e79;
        margin-bottom: 0px;
    }



    /* Back button */
    .st-key-back_wrap button {
        background-color: #1f4e79;
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: 600;
    }

    /* 所有按钮 */
    div.stButton > button {
        background-color: #2f5b82 !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        height: 36px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Compact button containers in top card */
    .st-key-back_wrap,
    .st-key-report_wrap {
        margin-bottom: -4px !important;
    }
    
    /* Compact popover button */
    div[class*="st-key-patient_info_card"] .stPopover > button {
        height: 36px !important;
        font-size: 14px !important;
    }

    div.stButton > button:hover {
        background-color: #244766 !important;
        color: white !important;
    }

    /* 占位头像 */
    .avatar-placeholder {
        width: 90px;
        height: 90px;
        border-radius: 18px;
        background: #eef5fb;
        border: 1px dashed #c5d6ea;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        font-size: 12px;
        color: #6b7a8c;
        text-align: center;
    }
    
    .details-page-title {
        font-size: 42px;
        font-weight: 700;
        color: #1f4e79;
        margin-top: 8px;
        margin-bottom: 18px;
    }
    
    .details-page-subtitle {
        font-size: 18px;
        color: #5f6b7a;
        margin-bottom: 36px;
    }
    
    .details-section-heading {
        font-size: 22px;
        font-weight: 700;
        color: #1f1f1f;
        margin-bottom: 16px;
    }
    
    .st-key-details_image_card {
        background: #f8fbff;
        border: 1px solid #dbe7f3;
        border-radius: 20px;
        padding: 24px;
        min-height: 420px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    
    .details-image-placeholder {
        width: 100%;
        height: 340px;
        border-radius: 18px;
        background: #eef5fb;
        border: 1px dashed #c5d6ea;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        font-size: 16px;
        color: #6b7a8c;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)