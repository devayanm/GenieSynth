import streamlit as st
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
import google.generativeai as genai
import requests
import matplotlib.pyplot as plt
import io
from wordcloud import WordCloud
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_extras.let_it_rain import rain
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stoggle import stoggle
from streamlit_extras.switch_page_button import switch_page

# Load environment variables
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

# Initialize the Google Generative AI model
genai.configure(api_key=google_api_key)

# Function to get response from Gemini Pro


def get_gemini_response(prompt):
    try:
        response = genai.generate_text(prompt=prompt)
        return response.result  # Adjust this based on the actual response structure
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Function to extract text from a PDF using PyMuPDF with keyword search


def extract_text_from_pdf(pdf_path, keywords=None):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            page_text = page.get_text()
            if keywords:
                for keyword in keywords:
                    if keyword.lower() in page_text.lower():
                        text += page_text
                        break
            else:
                text += page_text
    return text

# Function to generate a word cloud from text


def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400,
                          background_color='white').generate(text)
    return wordcloud

# Function to search literature (example API endpoint)


def search_literature(query):
    try:
        response = requests.get(
            f"https://api.literature-search.com?query={query}")
        return response.json()
    except Exception as e:
        st.error(f"Error searching literature: {e}")
        return None

# Function to send email notifications


def send_email(to_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        text = msg.as_string()
        server.sendmail(email_address, to_email, text)
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Error sending email: {e}")


# Define experiment templates
templates = {
    "Drug Development": "Template for developing new pharmaceutical compounds.",
    "Eco-friendly Pesticide": "Template for creating environmentally safe pesticides.",
    "High Tensile Polymer": "Template for designing polymers with high tensile strength."
}

# Session state management
if 'user_inputs' not in st.session_state:
    st.session_state['user_inputs'] = []

if 'responses' not in st.session_state:
    st.session_state['responses'] = []

# Custom CSS styling
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
    }
    .stSidebar {
        background-color: #28334AFF;
        color: white;
    }
    .stButton button {
        background-color: #FF6F61;
        color: white;
    }
    .stTextInput input {
        background-color: #f0f0f0;
    }
    .stFormSubmitButton button {
        background-color: #2E8B57;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("✨ GenieSynth")
st.subheader("Pioneering the Future of Chemical Science")

# Sidebar with custom layout
st.sidebar.header("📁 Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")
keywords = st.sidebar.text_input("Search Keywords (comma-separated):")

if uploaded_file is not None:
    try:
        keyword_list = [k.strip()
                        for k in keywords.split(',')] if keywords else None
        pdf_text = extract_text_from_pdf(uploaded_file, keyword_list)
        st.sidebar.text_area("PDF Content", pdf_text, height=300)
        if pdf_text:
            wordcloud = generate_wordcloud(pdf_text)
            st.sidebar.image(wordcloud.to_array(), use_column_width=True)
    except Exception as e:
        st.sidebar.error(f"Error reading PDF: {e}")

add_vertical_space(2)

st.sidebar.header("🔬 Experiment Templates")
template_selection = st.sidebar.selectbox(
    "Choose a template:", list(templates.keys()))
st.sidebar.write(templates[template_selection])

add_vertical_space(2)

st.sidebar.header("📝 Research Query")
user_input = st.sidebar.text_input("Enter your research query:")

# Main layout with columns
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Gemini Pro Analysis")
    if st.button("Submit Query"):
        if user_input:
            response = get_gemini_response(user_input)
            if response:
                st.session_state['user_inputs'].append(user_input)
                st.session_state['responses'].append(response)
                st.write("### Gemini Pro Response")
                st.write(response)
        else:
            st.error("Please enter a query to proceed.")

with col2:
    stoggle("🔍 Literature Search", "Search for related scientific literature.")
    if st.button("Search Literature"):
        if user_input:
            literature_results = search_literature(user_input)
            if literature_results:
                st.write("### Literature Search Results")
                st.write(literature_results)
        else:
            st.error("Please enter a query to proceed.")

# User feedback form
st.header("💬 Feedback")
with st.form(key='feedback_form'):
    feedback = st.text_area("Please provide your feedback:")
    submit_button = st.form_submit_button("Submit Feedback")

if submit_button:
    st.success("Thank you for your feedback!")

# Email results to user
if st.session_state['responses']:
    st.header("📧 Email Results")
    email = st.text_input("Enter your email address:")
    if st.button("Send Email"):
        if email:
            email_content = "\n\n".join([f"Query: {q}\nResponse: {r}" for q, r in zip(
                st.session_state['user_inputs'], st.session_state['responses'])])
            send_email(email, "GenieSynth Analysis Results", email_content)
        else:
            st.error("Please enter a valid email address.")

