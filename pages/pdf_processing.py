import streamlit as st
from utils import (
    extract_text_from_pdf, 
    generate_wordcloud, 
    analyze_sentiment, 
    plot_sentiment_analysis, 
    plot_word_frequency, 
    extract_entities, 
    extract_tables_from_pdf
)
import fitz
import pandas as pd
from io import BytesIO
import re

def pdf_processing_page():
    st.title("📁 PDF Processing")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        pdf_stream = BytesIO(file_bytes)

        st.write("### PDF Metadata")
        try:
            with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
                pdf_metadata = pdf.metadata
                st.write(f"**Title:** {pdf_metadata.get('title', 'N/A')}")
                st.write(f"**Author:** {pdf_metadata.get('author', 'N/A')}")
                st.write(f"**Creation Date:** {pdf_metadata.get('creationDate', 'N/A')}")
                st.write(f"**Number of Pages:** {pdf.page_count}")

        except Exception as e:
            st.error(f"Error retrieving PDF metadata: {e}")

        page_range = st.text_input("Enter page range (e.g., 1-3) or leave empty for all pages:")
        keywords = st.text_input("Search Keywords (comma-separated):")

        try:
            keyword_list = [k.strip() for k in keywords.split(',')] if keywords else None
            start_page, end_page = (None, None)
            if page_range:
                start_page, end_page = map(int, page_range.split('-'))

            file_stream = BytesIO(uploaded_file.read())

            pdf_text = extract_text_from_pdf(file_stream, keywords=keyword_list, start_page=start_page, end_page=end_page)
            if pdf_text:
                st.text_area("PDF Content", pdf_text, height=300)

                st.write("### Word Cloud")
                wordcloud_max_words = st.slider("Max Words", 10, 200, 100)
                wordcloud_width = st.slider("Width", 400, 800, 600)
                wordcloud_height = st.slider("Height", 400, 800, 400)
                wordcloud = generate_wordcloud(pdf_text, max_words=wordcloud_max_words, width=wordcloud_width, height=wordcloud_height)
                st.image(wordcloud.to_array(), use_column_width=True)

                st.write("### Sentiment Analysis")
                sentiment_scores = analyze_sentiment(pdf_text)
                sentiment_plot = plot_sentiment_analysis(sentiment_scores)
                if isinstance(sentiment_plot, plt.Figure):
                    st.pyplot(sentiment_plot)

                st.write("### Word Frequency")
                word_freq_plot = plot_word_frequency(pdf_text)
                if isinstance(word_freq_plot, plt.Figure):
                    st.pyplot(word_freq_plot)

                st.write("### Entity Recognition")
                entities = extract_entities(pdf_text)
                st.dataframe(entities)

                st.write("### Extracted Tables")
                file_stream.seek(0)  
                tables = extract_tables_from_pdf(file_stream)
                if tables:
                    for i, table in enumerate(tables):
                        st.write(f"Table {i+1}")
                        if isinstance(table, pd.DataFrame):  
                            st.dataframe(table)
                            st.download_button("Download Table as CSV", table.to_csv(), file_name=f"table_{i+1}.csv", mime="text/csv")
                        else:
                            st.write("Invalid table format.")
                else:
                    st.write("No tables found.")

                st.write("### Download Processed Text")
                if st.button("Download Text"):
                    buffer = BytesIO()
                    buffer.write(pdf_text.encode())
                    buffer.seek(0)
                    st.download_button("Download Text File", buffer, file_name="processed_text.txt", mime="text/plain")
                    
                st.write("### Search and Highlight Text")
                search_term = st.text_input("Search within the extracted text:")
                if search_term:
                    highlighted_text = re.sub(re.escape(search_term), f"**{search_term}**", pdf_text, flags=re.IGNORECASE)
                    st.text_area("Highlighted Text", highlighted_text, height=300)

            else:
                st.write("No text extracted from the PDF.")

        except Exception as e:
            st.error(f"Error processing PDF: {e}")

    st.write("### Interactive PDF Viewer")
    if uploaded_file is not None:
        st.write("#### View PDF")
        st.download_button("Download PDF", uploaded_file, file_name="uploaded_file.pdf")

    st.write("### PDF Annotation")
    if uploaded_file is not None:
        st.write("#### Annotate PDF")
        st.text_area("Add your annotations here:", height=200)

if __name__ == "__main__":
    pdf_processing_page()
