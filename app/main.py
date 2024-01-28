import streamlit as st
import random
import time

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
if st.session_state.info_submitted:
    # File Upload
    st.subheader("File Upload")
    uploaded_files = st.file_uploader("Upload your files", accept_multiple_files=True)
    if uploaded_files:
        with st.spinner("Processing files..."):
            # Process your files here
            time.sleep(5)  # Replace with actual file processing logic
        st.success("Files processed successfully!")

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
