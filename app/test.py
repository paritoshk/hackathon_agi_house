import streamlit as st
import base64

def convert_to_downloadable_string(text):
    """Create a downloadable link for the text string."""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="extracted_text.txt">Download Concatenated Text</a>'
    return href

st.title("Code and Documentation Extractor")

# Comprehensive list of code file formats
code_file_types = [
    'py', 'md', 'js', 'jsx', 'ts', 'tsx', 'java', 'c', 'cpp', 'cs', 'h', 'sh', 
    'rb', 'php', 'swift', 'go', 'kt', 'rs', 'lua', 'groovy', 'r', 'sql', 'pl', 
    'scala', 'hs', 'm', 'vb', 'sass', 'scss', 'css', 'html', 'json', 'xml', 'yml', 'yaml'
]

# Step 1: File Upload
uploaded_files = st.file_uploader("Upload code files", accept_multiple_files=True, type=code_file_types)

# Step 2: Extract Text
all_text = ""
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read the contents of each file
        file_text = uploaded_file.getvalue().decode("utf-8")
        all_text += file_text + "\n\n"  # Add a new line between files

# Step 3: Download as Text File
if all_text:
    st.markdown(convert_to_downloadable_string(all_text), unsafe_allow_html=True)
