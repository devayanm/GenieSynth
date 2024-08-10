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


def get_gemini_response(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        response = genai.generate_text(prompt=prompt)
        return response.result
    except Exception as e:
        return f"Error generating response: {e}"


def extract_text_from_pdf(pdf_path, keywords=None, start_page=None, end_page=None):
    text = ""
    with fitz.open(pdf_path) as pdf:
        num_pages = pdf.page_count
        start_page = start_page or 0
        end_page = end_page or num_pages
        for i in range(start_page, min(end_page, num_pages)):
            page = pdf.load_page(i)
            page_text = page.get_text()
            if keywords:
                if any(keyword.lower() in page_text.lower() for keyword in keywords):
                    text += page_text
            else:
                text += page_text
    return text


def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400,
                          background_color='white').generate(text)
    return wordcloud


def search_literature(query):
    try:
        response = requests.get(
            f"https://api.literature-search.com?query={query}")
        return response.json()
    except Exception as e:
        return f"Error searching literature: {e}"


def send_email(to_email, subject, message, email_address, email_password):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, to_email, msg.as_string())
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {e}"


def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)


def extract_entities(text):
    entities = {
        "Entities": ["Drug A", "Polymer B"],
        "Type": ["Chemical", "Material"]
    }
    return pd.DataFrame(entities)


def extract_tables_from_pdf(pdf_path):
    tables = []
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            tables.append(page.search_for_table())
    return tables


def plot_sentiment_analysis(sentiment_scores):
    labels = ['Positive', 'Negative', 'Neutral']
    scores = [sentiment_scores['pos'],
              sentiment_scores['neg'], sentiment_scores['neu']]
    plt.bar(labels, scores, color=['green', 'red', 'gray'])
    return plt


def plot_word_frequency(text):
    vectorizer = CountVectorizer(stop_words='english')
    word_count = vectorizer.fit_transform([text])
    word_freq = pd.DataFrame({'word': vectorizer.get_feature_names_out(
    ), 'count': word_count.toarray().sum(axis=0)})
    word_freq = word_freq.sort_values('count', ascending=False).head(20)
    sns.barplot(x='count', y='word', data=word_freq)
    return plt
