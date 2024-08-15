import streamlit as st
from utils import extract_text_from_pdf, generate_wordcloud, analyze_sentiment, plot_sentiment_analysis, plot_word_frequency, extract_entities, extract_tables_from_pdf
import fitz

def pdf_processing_page():
    st.title("📁 PDF Processing")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        st.write("### PDF Metadata")
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
            pdf_metadata = pdf.metadata
            st.write(f"**Title:** {pdf_metadata.get('title', 'N/A')}")
            st.write(f"**Author:** {pdf_metadata.get('author', 'N/A')}")
            st.write(f"**Creation Date:** {pdf_metadata.get('creationDate', 'N/A')}")
            st.write(f"**Number of Pages:** {pdf.page_count}")

        page_range = st.text_input("Enter page range (e.g., 1-3) or leave empty for all pages:")
        keywords = st.text_input("Search Keywords (comma-separated):")

        try:
            keyword_list = [k.strip() for k in keywords.split(',')] if keywords else None
            start_page, end_page = (None, None)
            if page_range:
                start_page, end_page = map(int, page_range.split('-'))

            pdf_text = extract_text_from_pdf(uploaded_file, keywords=keyword_list, start_page=start_page, end_page=end_page)
            st.text_area("PDF Content", pdf_text, height=300)

            if pdf_text:
                st.write("### Word Cloud")
                wordcloud = generate_wordcloud(pdf_text)
                st.image(wordcloud.to_array(), use_column_width=True)

                st.write("### Sentiment Analysis")
                sentiment_scores = analyze_sentiment(pdf_text)
                plot_sentiment_analysis(sentiment_scores)

                st.write("### Word Frequency")
                plot_word_frequency(pdf_text)

                st.write("### Entity Recognition")
                entities = extract_entities(pdf_text)
                st.dataframe(entities)

                st.write("### Extracted Tables")
                tables = extract_tables_from_pdf(uploaded_file)
                if tables:
                    for i, table in enumerate(tables):
                        st.write(f"Table {i+1}")
                        st.table(table)
                else:
                    st.write("No tables found.")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
