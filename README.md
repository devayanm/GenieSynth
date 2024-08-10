# GenieSynth

**GenieSynth** is a cutting-edge web application designed to provide personalized chemical solutions and experimental recommendations using the sophisticated Gemini Pro model. It aids researchers by generating custom experiment designs, chemical synthesis routes, and insightful data analysis.

## Features

- **Chemical Research Query**: Enter research queries to get customized experiment recommendations.
- **PDF Upload**: Upload PDFs to extract and analyze text content for research purposes.

## Installation

Follow these steps to set up and run GenieSynth on your local machine:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/devayanm/geniesynth.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd geniesynth
   ```

3. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project and add your Google API key:

   ```plaintext
   GOOGLE_API_KEY=your_api_key_here
   ```

   Replace `your_api_key_here` with your actual API key.

6. **Run the Application**

   Start the Streamlit application with the following command:

   ```bash
   streamlit run main.py
   ```

   The application will open in your default web browser.

## Usage

1. **Upload PDF**: Use the sidebar to upload a PDF file. The text content from the PDF will be displayed in the sidebar.
2. **Enter Research Query**: In the main area, enter your chemical research query.
3. **Submit**: Click the "Submit" button to get recommendations and insights from Gemini Pro.

## Contributing

If you would like to contribute to GenieSynth, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

