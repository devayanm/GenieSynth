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

# Update session state based on sidebar selection
if page_selection != st.session_state.page:
    st.session_state.page = page_selection

st.write(f"Current page: {st.session_state.page}")  # Debugging line

# Display the selected page
pages[st.session_state.page]()
