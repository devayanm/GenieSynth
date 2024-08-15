import streamlit as st
from pages.main_page import main_page
from pages.experiment_templates import experiment_templates_page
from pages.pdf_processing import pdf_processing_page
from pages.real_time_collaboration import real_time_collaboration_page

st.set_page_config(page_title="GenieSynth", page_icon="✨", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = "Main Page"

pages = {
    "Main Page": main_page,
    "Experiment Templates": experiment_templates_page,
    "PDF Processing": pdf_processing_page,
    "Real-time Collaboration": real_time_collaboration_page
}

st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Go to", list(pages.keys()))

if page_selection != st.session_state.page:
    st.session_state.page = page_selection

st.write(f"### {st.session_state.page}")

pages[st.session_state.page]()

st.markdown("""
    <style>
    .css-1v3fvcr { 
        display: none; 
    }
    .css-1v3fvcr {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
    }
    .stButton button {
        background-color: #0066cc;
        color: white;
    }
    .stSidebar {
        background-color: #f8f9fa;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #e6f7ff;
    }
    </style>
""", unsafe_allow_html=True)
