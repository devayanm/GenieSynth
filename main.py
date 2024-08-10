import streamlit as st
from dotenv import load_dotenv
import os
from google.generativeai import Client
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')

# Initialize Google Generative AI Client
client = Client(api_key=google_api_key)

# Function to get response from Gemini Pro
def get_gemini_response(prompt):
    response = client.generate(prompt=prompt)
    return response

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit UI
st.title("AI Chemist")

# Sidebar for PDF upload
st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.sidebar.text_area("PDF Content", pdf_text, height=300)

# User input for chemical research
st.header("Chemical Research Query")
user_input = st.text_input("Enter your research query:")

if st.button("Submit"):
    if user_input:
        response = get_gemini_response(user_input)
        st.write("### Gemini Pro Response")
        st.write(response)
    else:
        st.error("Please enter a query to proceed.")
