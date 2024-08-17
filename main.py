import streamlit as st
from page.main_page import main_page
from page.experiment_templates import experiment_templates_page
from page.pdf_processing import pdf_processing_page
from page.real_time_collaboration import real_time_collaboration_page

st.set_page_config(
    page_title="GenieSynth",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get help": None, "Report a bug": None, "About": None}
)

if 'page' not in st.session_state:
    st.session_state.page = "Main Page"

pages = {
    "Main Page": main_page,
    "Experiment Templates": experiment_templates_page,
    "PDF Processing": pdf_processing_page,
    "Real-time Collaboration": real_time_collaboration_page
}

query_params = st.query_params
page_from_query = query_params.get("page")

if page_from_query and page_from_query in pages:
    st.session_state.page = page_from_query

st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content button {
        background-color: #f4f4f4;
        color: #333;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        text-align: left;
    }
    .sidebar .sidebar-content button:hover {
        background-color: #ddd;
    }
    .active-button {
        background-color: #4CAF50;
        color: white;
        border: 1px solid #4CAF50;
    }
    .active-button:hover {
        background-color: #45A049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Navigation")

def sidebar_button(page_name, icon, active_page):
    button_class = "active-button" if active_page == page_name else ""
    if st.sidebar.button(f"{icon} {page_name}", key=page_name, help=f"Go to {page_name}", use_container_width=True):
        st.session_state.page = page_name
        st.query_params["page"] = page_name
    st.markdown(f'<style>.sidebar .sidebar-content button[data-testid="{page_name}"] {{ {button_class} }}</style>', unsafe_allow_html=True)

icons = {
    "Main Page": "🏠",
    "Experiment Templates": "🧪",
    "PDF Processing": "📄",
    "Real-time Collaboration": "💬"
}

for page_name in pages.keys():
    sidebar_button(page_name, icons[page_name], st.session_state.page)

if st.session_state.page == "Main Page":
    main_page()
elif st.session_state.page == "Experiment Templates":
    experiment_templates_page()
elif st.session_state.page == "PDF Processing":
    pdf_processing_page()
elif st.session_state.page == "Real-time Collaboration":
    real_time_collaboration_page()
