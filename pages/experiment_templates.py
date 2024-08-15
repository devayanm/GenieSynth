import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GENIE_API_KEY")

def generate_gemini_response(prompt):
    try:
        genai.configure(api_key=API_KEY)
        response = genai.generate_text(prompt=prompt)
        return response.result
    except Exception as e:
        st.error(f"Error connecting to Gemini Pro: {e}")
        return None

def experiment_templates_page():
    st.title("🔬 Experiment Templates")

    st.write("### Dynamic Template Generation")

    # Input fields for user to specify their requirements
    category = st.text_input("Enter Category (e.g., Pharmaceuticals, Materials Science):")
    template_type = st.text_input("Enter Template Type (e.g., Drug Development, High Tensile Polymer):")
    description = st.text_area("Describe the experiment or template requirements:")

    # Generate template using AI based on user input
    if st.button("Generate Template"):
        if category and template_type and description:
            prompt = (
                f"Create a detailed experiment template for the category '{category}' "
                f"and template type '{template_type}' with the following description: '{description}'."
            )
            template_content = generate_gemini_response(prompt)
            if template_content:
                st.write("### Generated Template")
                st.markdown(template_content)
                # Option to save or modify the generated template
                st.session_state.generated_template = template_content
            else:
                st.write("Failed to generate template. Please try again.")
        else:
            st.warning("Please fill in all fields to generate a template.")

    # Section for saving, commenting, and exporting the generated template
    if 'generated_template' in st.session_state:
        st.write("### Save or Modify Template")
        new_template_version = st.text_area("Modify Template:", st.session_state.generated_template)
        st.write("### Template Preview")
        st.markdown(new_template_version)

        if st.button("Save Version"):
            if 'template_versions' not in st.session_state:
                st.session_state['template_versions'] = {}
            if 'template_comments' not in st.session_state:
                st.session_state['template_comments'] = {}
            if template_type not in st.session_state['template_versions']:
                st.session_state['template_versions'][template_type] = []
                st.session_state['template_comments'][template_type] = []
            st.session_state['template_versions'][template_type].append(new_template_version)
            st.success("Version saved successfully!")

        st.write("### Template Versions")
        version_comments = st.text_input("Add a comment for this version:")
        if st.button("Add Comment"):
            st.session_state['template_comments'][template_type].append(version_comments)
            st.success("Comment added successfully!")

        for i, (version, comment) in enumerate(zip(st.session_state['template_versions'][template_type], st.session_state['template_comments'][template_type])):
            st.write(f"**Version {i+1}**: {version}")
            st.write(f"**Comment**: {comment}")
            if st.button(f"Restore Version {i+1}", key=f"restore_{i}"):
                st.session_state['template_versions'][template_type] = [version]
                st.success("Version restored successfully!")

        st.write("### Share or Export Templates")
        if st.button("Export Template"):
            template_str = '\n'.join(st.session_state['template_versions'][template_type])
            st.download_button("Download Template", template_str, f"{template_type}.txt")

        uploaded_template = st.file_uploader("Import Template", type="txt")
        if uploaded_template is not None:
            new_template = uploaded_template.read().decode("utf-8")
            st.session_state['template_versions'][template_type].append(new_template)
            st.success("Template imported successfully!")

    st.write("### Generate Personalized Recommendations")
    user_input = st.text_area("Enter experiment details or chemical properties:")
    if st.button("Get Recommendations"):
        if user_input.strip():
            prompt = f"Generate personalized chemical solutions and experimental recommendations based on the following input: {user_input}"
            recommendations = generate_gemini_response(prompt)
            if recommendations:
                st.write("### Recommendations")
                st.markdown(recommendations)
            else:
                st.write("No recommendations found.")
        else:
            st.warning("Please enter some details to get recommendations.")

if __name__ == "__main__":
    experiment_templates_page()
