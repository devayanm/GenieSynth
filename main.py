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
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns
import pandas as pd

# Load environment variables
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

# Initialize the Google Generative AI model
genai.configure(api_key=google_api_key)

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

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
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Function to search literature (example API endpoint)
def search_literature(query):
    try:
        response = requests.get(f"https://api.literature-search.com?query={query}")
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

# Function for sentiment analysis
def analyze_sentiment(text):
    return sia.polarity_scores(text)

# Function for entity recognition (placeholder, you can use SpaCy or any other NLP library)
def extract_entities(text):
    entities = {
        "Entities": ["Drug A", "Polymer B"],
        "Type": ["Chemical", "Material"]
    }
    return pd.DataFrame(entities)

# Function for advanced PDF processing (extract tables)
def extract_tables_from_pdf(pdf_path):
    tables = []
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            tables.append(page.search_for_table())
    return tables

# Function to plot sentiment analysis
def plot_sentiment_analysis(sentiment_scores):
    labels = ['Positive', 'Negative', 'Neutral']
    scores = [sentiment_scores['pos'], sentiment_scores['neg'], sentiment_scores['neu']]
    plt.bar(labels, scores, color=['green', 'red', 'gray'])
    st.pyplot(plt)

# Function to plot word frequency
def plot_word_frequency(text):
    vectorizer = CountVectorizer(stop_words='english')
    word_count = vectorizer.fit_transform([text])
    word_freq = pd.DataFrame({'word': vectorizer.get_feature_names_out(), 'count': word_count.toarray().sum(axis=0)})
    word_freq = word_freq.sort_values('count', ascending=False).head(20)
    sns.barplot(x='count', y='word', data=word_freq)
    st.pyplot(plt)

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

if 'template_versions' not in st.session_state:
    st.session_state['template_versions'] = {}

# Custom CSS styling
st.markdown("""
    <style>
    body {
        background-color: #f0f0f0;
    }
    .stSidebar {
        background-color: #33475b;
        color: white;
    }
    .stButton button {
        background-color: #FF6F61;
        color: white;
    }
    .stTextInput input {
        background-color: #e6e6e6;
    }
    .stFormSubmitButton button {
        background-color: #2E8B57;
        color: white;
    }
    .stHeader {
        background-color: #FF6F61;
        color: white;
    }
    .stTitle {
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 2.5rem;
        color: #28334AFF;
    }
    .stSubheader {
        font-family: 'Arial', sans-serif;
        font-size: 1.5rem;
        color: #28334AFF;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI with multi-page navigation
st.set_page_config(page_title="GenieSynth", page_icon="✨", layout="wide")

def main_page():
    st.title("✨ GenieSynth")
    st.subheader("Pioneering the Future of Chemical Science")
    rain(emoji="🧪", font_size=30, falling_speed=10, animation_length="infinite")

def pdf_processing_page():
    st.title("📁 PDF Processing")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    keywords = st.text_input("Search Keywords (comma-separated):")
    if uploaded_file is not None:
        try:
            keyword_list = [k.strip() for k in keywords.split(',')] if keywords else None
            pdf_text = extract_text_from_pdf(uploaded_file, keyword_list)
            st.text_area("PDF Content", pdf_text, height=300)
            if pdf_text:
                wordcloud = generate_wordcloud(pdf_text)
                st.image(wordcloud.to_array(), use_column_width=True)
                sentiment_scores = analyze_sentiment(pdf_text)
                plot_sentiment_analysis(sentiment_scores)
                plot_word_frequency(pdf_text)
        except Exception as e:
            st.error(f"Error processing PDF: {e}")

def experiment_templates_page():
    st.title("🔬 Experiment Templates")
    template_selection = st.selectbox("Choose a template:", list(templates.keys()))
    st.write(templates[template_selection])
    if template_selection not in st.session_state['template_versions']:
        st.session_state['template_versions'][template_selection] = [templates[template_selection]]

    # Save template version
    new_template_version = st.text_area("Modify Template:", templates[template_selection])
    if st.button("Save Version"):
        st.session_state['template_versions'][template_selection].append(new_template_version)
        st.success("Version saved successfully!")

    # Display template versions
    st.write("### Template Versions")
    for i, version in enumerate(st.session_state['template_versions'][template_selection]):
        st.write(f"Version {i+1}: {version}")

def real_time_collaboration_page():
    st.title("👥 Real-time Collaboration")
    chat_input = st.text_input("Enter your message:")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if st.button("Send"):
        st.session_state['chat_history'].append(chat_input)
    st.write("### Chat History")
    for msg in st.session_state['chat_history']:
        st.write(f"- {msg}")

# Multi-page navigation
pages = {
    "Main Page": main_page,
    "PDF Processing": pdf_processing_page,
    "Experiment Templates": experiment_templates_page,
    "Real-time Collaboration": real_time_collaboration_page
}

st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Go to", list(pages.keys()))

# Render the selected page
pages[page_selection]()
