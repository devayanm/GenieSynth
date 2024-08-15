import streamlit as st

def experiment_templates_page():
    st.title("🔬 Experiment Templates")

    templates = {
        "Pharmaceuticals": {
            "Drug Development": "Template for developing new pharmaceutical compounds.",
            "Vaccine Research": "Template for designing and testing vaccines."
        },
        "Materials Science": {
            "Eco-friendly Pesticide": "Template for creating environmentally safe pesticides.",
            "High Tensile Polymer": "Template for designing polymers with high tensile strength."
        }
    }

    if 'template_versions' not in st.session_state:
        st.session_state['template_versions'] = {}

    if 'template_comments' not in st.session_state:
        st.session_state['template_comments'] = {}

    selected_category = st.selectbox("Choose a category:", list(templates.keys()))
    selected_template = st.selectbox("Choose a template:", list(templates[selected_category].keys()))

    st.write(f"### {selected_template} Template")
    st.write(templates[selected_category][selected_template])

    if selected_template not in st.session_state['template_versions']:
        st.session_state['template_versions'][selected_template] = [templates[selected_category][selected_template]]

    if selected_template not in st.session_state['template_comments']:
        st.session_state['template_comments'][selected_template] = []

    new_template_version = st.text_area("Modify Template:", templates[selected_category][selected_template])
    st.write("### Template Preview")
    st.markdown(new_template_version)

    if st.button("Save Version"):
        st.session_state['template_versions'][selected_template].append(new_template_version)
        st.success("Version saved successfully!")

    st.write("### Template Versions")
    version_comments = st.text_input("Add a comment for this version:")
    if st.button("Add Comment"):
        st.session_state['template_comments'][selected_template].append(version_comments)
        st.success("Comment added successfully!")

    for i, (version, comment) in enumerate(zip(st.session_state['template_versions'][selected_template], st.session_state['template_comments'][selected_template])):
        st.write(f"**Version {i+1}**: {version}")
        st.write(f"**Comment**: {comment}")
        if st.button(f"Restore Version {i+1}", key=f"restore_{i}"):
            st.session_state['template_versions'][selected_template] = [version]
            st.success("Version restored successfully!")

    st.write("### Share or Export Templates")
    if st.button("Export Template"):
        template_str = '\n'.join(st.session_state['template_versions'][selected_template])
        st.download_button("Download Template", template_str, f"{selected_template}.txt")

    uploaded_template = st.file_uploader("Import Template", type="txt")
    if uploaded_template is not None:
        new_template = uploaded_template.read().decode("utf-8")
        st.session_state['template_versions'][selected_template].append(new_template)
        st.success("Template imported successfully!")
