import streamlit as st

def main_page():
    st.title("✨ GenieSynth")
    st.subheader("Pioneering the Future of Chemical Science")

    st.write("""
    **GenieSynth** is an advanced AI-powered platform designed to revolutionize the way researchers and scientists approach chemical science. 
    Harness cutting-edge technology to streamline your research and enhance your experimentation processes.
    """)

    st.write("### 🔑 Key Features")
    st.write("""
    - **AI-Driven Experiment Design**: Create customized experiment templates using AI to meet your specific research requirements.
    - **PDF Processing and Analysis**: Efficiently extract and analyze content from research papers with tools for sentiment analysis and keyword extraction.
    - **Real-time Collaboration**: Collaborate with your team dynamically using live chat and shared workspaces.
    - **Advanced Visualization**: Generate insightful visualizations such as word clouds and sentiment analysis plots to effectively present your research data.
    """)

    st.write("### 🚀 How It Works")
    st.write("""
    1. **Experiment Design**: Choose or tailor an experiment template from our extensive library.
    2. **PDF Processing**: Upload research papers and use advanced tools to extract and analyze critical data.
    3. **Collaborate**: Engage with team members through our real-time collaboration features to discuss findings and work together seamlessly.
    4. **Visualize**: Utilize visualization tools to create meaningful representations of your data and share insights with your team.
    """)

    st.write("### 🧪 Get Started")
    st.write("""
    Ready to transform your research process? Explore GenieSynth’s capabilities by selecting an option from the sidebar!
    """)

    # Display an engaging image
    st.image("https://your-image-link.com/image.jpg",
             caption="GenieSynth in Action", use_column_width=True)

    # Enhanced navigation with buttons
    st.write("### ⚡ Quick Access")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔬 Experiment Templates"):
            st.session_state.page = "Experiment Templates"
            st.experimental_rerun()
    with col2:
        if st.button("📁 PDF Processing"):
            st.session_state.page = "PDF Processing"
            st.experimental_rerun()
    with col3:
        if st.button("👥 Real-time Collaboration"):
            st.session_state.page = "Real-time Collaboration"
            st.experimental_rerun()

    st.write("---")
    st.write("""
    **Need help?** Visit our [documentation](https://your-docs-link.com) or contact our [support team](mailto:support@geniesynth.com).
    """)

    # Optional: Add some custom CSS for a polished look
    st.markdown("""
        <style>
        .css-1v3fvcr {
            padding: 20px;
            border-radius: 8px;
            background-color: #f5f5f5;
        }
        .stButton button {
            background-color: #0066cc;
            color: white;
        }
        .stImage img {
            border-radius: 8px;
        }
        .stMarkdown {
            font-size: 1.1em;
        }
        </style>
    """, unsafe_allow_html=True)
