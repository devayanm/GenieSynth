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

    st.write("### 📷 Explore GenieSynth")
    st.image("https://your-image-link.com/image1.jpg", caption="GenieSynth Overview", use_column_width=True)
    st.image("https://your-image-link.com/image2.jpg", caption="Advanced Features", use_column_width=True)
    
    st.write("### ⚡ Quick Access")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔬 Experiment Templates"):
            st.session_state.page = "Experiment Templates"
    with col2:
        if st.button("📁 PDF Processing"):
            st.session_state.page = "PDF Processing"
    with col3:
        if st.button("👥 Real-time Collaboration"):
            st.session_state.page = "Real-time Collaboration"

    st.write("---")
    
    st.write("### 🌟 Join Us Now")
    st.button("Sign Up for a Demo", key="signup_button", on_click=lambda: st.markdown("[Sign Up for a Demo](https://your-signup-link.com)"))

    st.write("""
    **Need help?** Visit our [documentation](https://your-docs-link.com) or contact our [support team](mailto:support@geniesynth.com).
    """)

    st.write("---")
    st.write("""
    ### 📢 Follow Us
    - [Twitter](https://twitter.com/geniesynth)
    - [LinkedIn](https://linkedin.com/company/geniesynth)
    - [Blog](https://your-blog-link.com)
    """)

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
            border-radius: 5px;
        }
        .stImage img {
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .stMarkdown {
            font-size: 1.1em;
        }
        .stButton {
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
