import streamlit as st
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
from google.generativeai import Client
import requests

# Load environment variables
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')

# Initialize Google Generative AI Client
client = Client(api_key=google_api_key)

# Function to get response from Gemini Pro


def get_gemini_response(prompt):
    response = client.generate(prompt=prompt)
    return response

# Function to extract text from a PDF using PyMuPDF


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text


# Define experiment templates
templates = {
    "Drug Development": "Template for developing new pharmaceutical compounds.",
    "Eco-friendly Pesticide": "Template for creating environmentally safe pesticides.",
    "High Tensile Polymer": "Template for designing polymers with high tensile strength."
}

# Function to search literature (example API endpoint)


def search_literature(query):
    response = requests.get(f"https://api.literature-search.com?query={query}")
    return response.json()


# Streamlit UI
st.title("GenieSynth")

# Sidebar for PDF upload
st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.sidebar.text_area("PDF Content", pdf_text, height=300)
    except Exception as e:
        st.sidebar.error(f"Error reading PDF: {e}")

# Experiment templates selection
st.sidebar.header("Experiment Templates")
template_selection = st.sidebar.selectbox(
    "Choose a template:", list(templates.keys()))
st.sidebar.write(templates[template_selection])

# User input for chemical research
st.header("Chemical Research Query")
user_input = st.text_input("Enter your research query:")

if st.button("Submit"):
    if user_input:
        try:
            response = get_gemini_response(user_input)
            st.write("### Gemini Pro Response")
            st.write(response)
        except Exception as e:
            st.error(f"Error generating response: {e}")
    else:
        st.error("Please enter a query to proceed.")

# User feedback form
st.header("Feedback")
with st.form(key='feedback_form'):
    feedback = st.text_area("Please provide your feedback:")
    submit_button = st.form_submit_button("Submit Feedback")

if submit_button:
    st.success("Thank you for your feedback!")
    # Here, you could add functionality to store or process the feedback
