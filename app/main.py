import streamlit as st
import zipfile
import os
import tempfile
import requests
import base64
import sys
sys.path.append("db")
from db.index import generate_matches
import time
from utils import * 
import together
together.api_key = LEON_TOGETHER_KEY

def get_file_content_as_base64(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return data

st.title("Decoder AI")

# Initialize session state for user information and submission status
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "info_submitted" not in st.session_state:
    st.session_state.info_submitted = False

# Step 1: Collect user information
if not st.session_state.info_submitted:
    with st.form("user_info_form"):
        name = st.text_input("Enter your name")
        organization = st.text_input("Enter your organization")
        user_type = st.selectbox("Select your role", ["Manager", "New Employee", "Developer", "Administration", "Product"])
        preference = st.radio("Preference", ["Code", "No Code"])
        goal = st.radio("Your goal", ["Query codebase", "Search and find certain flows", "Understand and manage risks"])
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.user_info = {
                "name": name,
                "organization": organization,
                "user_type": user_type,
                "preference": preference,
                "goal": goal
            }
            st.session_state.info_submitted = True
            st.balloons()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom HTML for spinner
spinner_html = """
<div style="display: flex; align-items: center; justify-content: center;">
    <div class="loader" style="border: 4px solid #f3f3f3; 
                               border-top: 4px solid #3498db; 
                               border-radius: 50%; 
                               width: 40px; 
                               height: 40px; 
                               animation: spin 2s linear infinite;">
    </div>
</div>
<style>
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
"""

# Step 2: File Upload and Chat, appear only after information submission
if st.session_state.get("info_submitted", False):
    st.subheader("Upload Your Repository")
    st.write("Please ZIP your entire repository and upload the ZIP file here.")
    
    uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")
    if uploaded_file is not None:
        with st.spinner("Processing ZIP file..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_path = os.path.join(tmpdir, "uploaded.zip")
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(tmpdir)
                st.success("ZIP file processed successfully!")

                # TODO: Send the files to your MongoDB vector database maker endpoint
                # This typically involves either making an API call or performing some database operation.
                # Example (you will need to replace this with your actual code):
                # for file_name in extracted_files:
                #     file_path = os.path.join(tmpdir, file_name)
                #     with open(file_path, 'rb') as f:
                #         # Replace 'your_endpoint' with your actual endpoint and adjust the request as needed
                #         response = requests.post('your_endpoint', files={'file': f})
                #         # Handle the response as needed

# Other parts of your Streamlit app (user info form, chat interface, etc.)
# ...
    # Chat Interface
    st.subheader("Chat with Us")
    # Initialize chat history if not already done
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Check if chat history is empty and initiate chat with a bot message
    if not st.session_state.messages:
        bot_init_message = "Hi, fellow curious code explorer! Thank you for uploading your codebase - is there anything I can help you with?"
        st.session_state.messages.append({"role": "assistant", "content": bot_init_message})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.empty():
                st.markdown(spinner_html, unsafe_allow_html=True)
                paths = generate_matches(prompt) 
                paths = [path[3:] for path in paths]
                concat_scripts = concat_files(paths)
                final_prompt = synthesize_prompt(prompt, concat_scripts, st.session_state.user_info)
                assistant_response = together.Complete.create(prompt=final_prompt, model="mistralai/Mixtral-8x7B-Instruct-v0.1")
                temp = assistant_response["output"]["choices"][0]["text"]

                for path in paths:
                    with st.sidebar.expander(path):
                        st.text(print_file(path))

                # paths = [path.split("mongo-python-driver/")[1] for path in paths]
                # final = ",".join(paths) + temp
                full_response = ""
                final = temp
                # Simulate stream of response with milliseconds delay
                for chunk in final.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    st.markdown(full_response + "▌")
            # st.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
