import fitz
import google.generativeai as genai
import requests
import matplotlib.pyplot as plt
import io
from wordcloud import WordCloud
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns
import pandas as pd
import spacy
import logging
import pdfplumber
import nltk
nltk.download('vader_lexicon')


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

nlp = spacy.load("en_core_web_sm")

def get_gemini_response(prompt, api_key):
    """
    Retrieves a response from Gemini AI using the provided prompt and API key.
    """
    try:
        genai.configure(api_key=api_key)
        response = genai.generate_text(prompt=prompt)
        return response.result
    except Exception as e:
        logging.error(f"Error generating response from Gemini AI: {e}")
        return f"Error generating response: {e}"

def extract_text_from_pdf(pdf_file, keywords=None, start_page=None, end_page=None):
    """
    Extracts text from a PDF file, optionally filtering by keywords and page range.
    """
    text = ""
    if not pdf_file:
        logging.error("No PDF file provided.")
        return "Error: No PDF file provided."

    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
            num_pages = pdf.page_count
            start_page = start_page or 0
            end_page = end_page or num_pages
            if start_page > end_page:
                raise ValueError("Start page cannot be greater than end page.")

            for i in range(start_page, min(end_page, num_pages)):
                page = pdf.load_page(i)
                page_text = page.get_text()
                if keywords:
                    if any(keyword.lower() in page_text.lower() for keyword in keywords):
                        text += page_text
                else:
                    text += page_text

        if not text:
            logging.warning("No text extracted from the PDF.")
            return "Warning: No text extracted from the PDF."
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return f"Error extracting text from PDF: {e}"

    return text

def generate_wordcloud(text, max_words=100, width=800, height=400):
    """
    Generates a word cloud image from the provided text with customizable settings.
    """
    try:
        if not text:
            raise ValueError("No text provided for word cloud generation.")
        
        wordcloud = WordCloud(
            width=width, 
            height=height, 
            background_color='white', 
            max_words=max_words
        ).generate(text)
        
        return wordcloud
    except Exception as e:
        logging.error(f"Error generating word cloud: {e}")
        return f"Error generating word cloud: {e}"

def search_literature(query):
    """
    Searches for literature based on the provided query using an external API.
    """
    try:
        response = requests.get(f"https://api.literature-search.com?query={query}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error searching literature: {e}")
        return f"Error searching literature: {e}"

def send_email(to_email, subject, message, email_address, email_password):
    """
    Sends an email with the specified subject and message using the provided email credentials.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, to_email, msg.as_string())
        
        return "Email sent successfully!"
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"Error sending email: {e}"

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the provided text.
    """
    try:
        if not text:
            raise ValueError("No text provided for sentiment analysis.")
        
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(text)
        return sentiment_scores
    except Exception as e:
        logging.error(f"Error analyzing sentiment: {e}")
        return f"Error analyzing sentiment: {e}"

def extract_entities(text):
    """
    Extracts entities from the provided text using spaCy.
    """
    try:
        if not text:
            raise ValueError("No text provided for entity extraction.")
        
        doc = nlp(text)
        entities = {"Entities": [ent.text for ent in doc.ents], "Type": [ent.label_ for ent in doc.ents]}
        return pd.DataFrame(entities)
    except Exception as e:
        logging.error(f"Error extracting entities: {e}")
        return f"Error extracting entities: {e}"

def extract_tables_from_pdf(pdf_file):
    """
    Extracts tables from a PDF file.
    """
    try:
        tables = []
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                tables.extend(page.extract_tables())
        return tables
    except Exception as e:
        logging.error(f"Error extracting tables from PDF: {e}")
        return f"Error extracting tables from PDF: {e}"


def plot_sentiment_analysis(sentiment_scores):
    """
    Plots sentiment analysis results as a bar chart.
    """
    try:
        if not sentiment_scores or not isinstance(sentiment_scores, dict):
            raise ValueError("Invalid sentiment scores provided.")

        labels = ['Positive', 'Negative', 'Neutral']
        scores = [sentiment_scores.get('pos', 0), sentiment_scores.get('neg', 0), sentiment_scores.get('neu', 0)]
        
        plt.figure(figsize=(8, 4))
        plt.bar(labels, scores, color=['green', 'red', 'gray'])
        plt.title('Sentiment Analysis')
        plt.xlabel('Sentiment')
        plt.ylabel('Score')
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        
        return buf
    except Exception as e:
        logging.error(f"Error plotting sentiment analysis: {e}")
        return f"Error plotting sentiment analysis: {e}"

def plot_word_frequency(text):
    """
    Plots word frequency from the provided text.
    """
    try:
        if not text:
            raise ValueError("No text provided for word frequency analysis.")

        vectorizer = CountVectorizer(stop_words='english')
        word_count = vectorizer.fit_transform([text])
        word_freq = pd.DataFrame({'word': vectorizer.get_feature_names_out(), 'count': word_count.toarray().sum(axis=0)})
        word_freq = word_freq.sort_values('count', ascending=False).head(20)
        
        if word_freq.empty:
            raise ValueError("No words to plot.")
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='count', y='word', data=word_freq, palette='viridis', hue=None) 
        plt.title('Word Frequency')
        plt.xlabel('Count')
        plt.ylabel('Word')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf
    except Exception as e:
        logging.error(f"Error plotting word frequency: {e}")
        return f"Error plotting word frequency: {e}"
