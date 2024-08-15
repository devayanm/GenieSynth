import streamlit as st

def main_page():
    st.title("✨ GenieSynth")
    st.subheader("Pioneering the Future of Chemical Science")

    st.write("""
    **GenieSynth** is an advanced AI-powered platform designed to revolutionize the way researchers and scientists approach chemical science. 
    With a suite of innovative tools, GenieSynth offers personalized chemical solutions, experimental recommendations, and a collaborative environment 
    for cutting-edge research in pharmaceutical, green chemistry, and polymer science.
    """)

    st.write("### 🔑 Key Features")
    st.write("""
    - **AI-Driven Experiment Design**: Harness the power of AI to create tailored experiment templates for your specific research needs.
    - **PDF Processing and Analysis**: Extract and analyze content from research papers, including sentiment analysis and keyword extraction.
    - **Real-time Collaboration**: Engage with your team in a dynamic environment with live chat and shared workspaces.
    - **Advanced Visualization**: Generate word clouds, sentiment analysis plots, and more to visualize your research data effectively.
    """)

    st.write("### 🚀 How It Works")
    st.write("""
    1. **Experiment Design**: Select or customize an experiment template from our library.
    2. **PDF Processing**: Upload your research papers and extract meaningful data with our advanced PDF processing tools.
    3. **Collaborate**: Use the real-time collaboration tools to discuss your findings and work together seamlessly.
    4. **Visualize**: Create visual representations of your data to gain insights and share with your team.
    """)

    st.write("### 🧪 Get Started")
    st.write("""
    Ready to transform your research process? Select an option from the sidebar to begin exploring GenieSynth's capabilities!
    """)

    st.image("https://your-image-link.com/image.jpg",
             caption="GenieSynth in Action", use_column_width=True)

    st.write("### ⚡ Quick Access")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔬 Experiment Templates"):
            st.session_state.page = "Experiment Templates"
            st.write("Button '🔬 Experiment Templates' clicked")
    with col2:
        if st.button("📁 PDF Processing"):
            st.session_state.page = "PDF Processing"
            st.write("Button '📁 PDF Processing' clicked")
    with col3:
        if st.button("👥 Real-time Collaboration"):
            st.session_state.page = "Real-time Collaboration"
            st.write("Button '👥 Real-time Collaboration' clicked")
    st.write("---")
    st.write("""
    **Need help?** Visit our [documentation](https://your-docs-link.com) or contact our [support team](mailto:support@geniesynth.com).
    """)
