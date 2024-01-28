import streamlit as st
import zipfile
import os
import tempfile
import requests

st.title("NameItLater")

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

# Step 2: File Upload and Chat, appear only after information submission
if st.session_state.get("info_submitted", False):
    st.subheader("Upload Your Repository")
    st.write("Please ZIP your entire repository and upload the ZIP file here.")
    
    uploaded_file = st.file_uploader("Upload ZIP", type="py")
    if uploaded_file is not None:
        with st.spinner("Processing ZIP file..."):
            # Create a temporary directory to extract the ZIP
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_path = os.path.join(tmpdir, "uploaded.zip")
                # Write the uploaded ZIP file to the temporary directory
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # Extract the ZIP file
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(tmpdir)
                st.success("ZIP file processed successfully!")

                # Process the extracted files as needed
                # For example, you can list the extracted files
                extracted_files = os.listdir(tmpdir)
                st.write("Extracted Files:", extracted_files)

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
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = random.choice(
                [
                    "Hello curious code explorer! How can I assist you today?",
                    "Hi, fellow curious code explorer! Is there anything I can help you with?",
                    "Do you need help?",
                ]
            )
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
