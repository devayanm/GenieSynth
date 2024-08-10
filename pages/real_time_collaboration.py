import streamlit as st


def real_time_collaboration_page():
    st.title("👥 Real-time Collaboration")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if 'user_mentions' not in st.session_state:
        st.session_state['user_mentions'] = []

    user_name = st.text_input("Your Name:")
    chat_input = st.text_area("Enter your message:")

    if st.button("Send"):
        if chat_input:
            mentions = [word[1:]
                        for word in chat_input.split() if word.startswith('@')]
            st.session_state['chat_history'].append(
                {"user": user_name, "message": chat_input, "mentions": mentions})
            if mentions:
                st.session_state['user_mentions'].extend(mentions)
            st.success("Message sent successfully!")

    st.write("### Chat History")
    for entry in st.session_state['chat_history']:
        message_display = f"**{entry['user']}**: {entry['message']}"
        if entry['mentions']:
            mention_list = ', '.join(
                [f"@{mention}" for mention in entry['mentions']])
            message_display += f" [Mentions: {mention_list}]"
        st.write(message_display)

    st.write("### Filter by Mentions")
    mention_filter = st.text_input("Filter by user (e.g., @john):")
    if mention_filter:
        filtered_messages = [entry for entry in st.session_state['chat_history']
                             if mention_filter[1:] in entry['mentions']]
        if filtered_messages:
            st.write("### Filtered Messages")
            for entry in filtered_messages:
                st.write(f"**{entry['user']}**: {entry['message']}")
        else:
            st.write("No messages found for this mention.")

    st.write("### Share Files")
    uploaded_file = st.file_uploader("Choose a file to share:")
    if uploaded_file is not None:
        st.session_state['chat_history'].append(
            {"user": user_name, "message": f"shared a file: {uploaded_file.name}", "mentions": []})
        st.success(f"File {uploaded_file.name} shared successfully!")

    st.write("### Export Chat History")
    if st.button("Export Chat"):
        chat_history_str = '\n'.join(
            [f"{entry['user']}: {entry['message']}" for entry in st.session_state['chat_history']])
        st.download_button("Download Chat History",
                           chat_history_str, "chat_history.txt")

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
        </style>
    """, unsafe_allow_html=True)
