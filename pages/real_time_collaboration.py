import streamlit as st
import datetime
from io import StringIO
from docx import Document

def real_time_collaboration_page():
    st.title("👥 Real-time Collaboration")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if 'user_mentions' not in st.session_state:
        st.session_state['user_mentions'] = []

    if 'users' not in st.session_state:
        st.session_state['users'] = []

    user_name = st.text_input("Your Name:", "")
    if user_name and user_name not in st.session_state['users']:
        st.session_state['users'].append(user_name)

    chat_input = st.text_area("Enter your message:")

    if st.button("Send"):
        if not user_name:
            st.warning("Please enter your name before sending a message.")
        elif not chat_input:
            st.warning("Message cannot be empty.")
        else:
            mentions = [word[1:] for word in chat_input.split() if word.startswith('@')]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state['chat_history'].append({"user": user_name, "message": chat_input, "mentions": mentions, "timestamp": timestamp})
            if mentions:
                st.session_state['user_mentions'].extend(mentions)
            st.success("Message sent successfully!")

    st.write("### Chat History")
    for entry in st.session_state['chat_history']:
        message_display = f"**{entry['timestamp']} - {entry['user']}**: {entry['message']}"
        if entry['mentions']:
            mention_list = ', '.join([f"@{mention}" for mention in entry['mentions']])
            message_display += f" [Mentions: {mention_list}]"
        st.write(message_display)

    st.write("### Filter by Mentions")
    mention_filter = st.text_input("Filter by user (e.g., @john):")
    if mention_filter:
        filtered_messages = [entry for entry in st.session_state['chat_history'] if mention_filter[1:] in entry['mentions']]
        if filtered_messages:
            st.write("### Filtered Messages")
            for entry in filtered_messages:
                st.write(f"**{entry['timestamp']} - {entry['user']}**: {entry['message']}")
        else:
            st.write("No messages found for this mention.")

    st.write("### Share Files")
    uploaded_file = st.file_uploader("Choose a file to share:", type=["pdf", "txt", "docx", "jpg", "png"])
    if uploaded_file is not None:
        st.session_state['chat_history'].append({"user": user_name, "message": f"shared a file: {uploaded_file.name}", "mentions": [], "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        st.success(f"File {uploaded_file.name} shared successfully!")

        if uploaded_file.type in ["image/jpeg", "image/png"]:
            st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)
        elif uploaded_file.type in ["application/pdf"]:
            st.write("PDF uploaded. Displaying first page:")
            pdf_content = uploaded_file.read()
            st.download_button("Download PDF", pdf_content, file_name=uploaded_file.name, mime=uploaded_file.type)
        elif uploaded_file.type in ["text/plain"]:
            st.write("Text file content:")
            content = uploaded_file.read().decode("utf-8")
            st.text_area("File Content", content, height=200)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            st.write("DOCX file content:")
            doc = Document(uploaded_file)
            doc_text = '\n'.join([p.text for p in doc.paragraphs])
            st.text_area("DOCX Content", doc_text, height=300)
        else:
            st.write("File type not supported for preview.")

    st.write("### Export Chat History")
    if st.button("Export Chat"):
        chat_history_str = '\n'.join([f"{entry['timestamp']} - {entry['user']}: {entry['message']}" for entry in st.session_state['chat_history']])
        buffer = StringIO()
        buffer.write(chat_history_str)
        buffer.seek(0)
        st.download_button("Download Chat History", buffer, file_name="chat_history.txt", mime="text/plain")

    st.markdown("""
        <style>
        .stTextInput input, .stTextArea textarea {
            background-color: #e6f7ff;
        }
        .stButton button {
            background-color: #0066cc;
            color: white;
        }
        .stDownloadButton button {
            background-color: #28a745;
            color: white;
        }
        .stFileUploader input[type="file"] {
            background-color: #e6f7ff;
        }
        </style>
    """, unsafe_allow_html=True)

