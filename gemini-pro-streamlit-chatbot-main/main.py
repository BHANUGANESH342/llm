import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="CHAT WITH BHANU'S AI!",
    page_icon="\U0001F4A1",  # Light bulb emoji
    layout="centered",  # Page layout option
)

# Add custom CSS for 3D effect
st.markdown(
    """
    <style>
    /* Add 3D effect to the chatbot container */
    .stChatMessage:nth-child(odd) {
        background-color: #f1f1f1;
        border-radius: 10px;
        box-shadow: 5px 5px 15px #aaaaaa,
                    -5px -5px 15px #ffffff;
        padding: 10px;
        margin: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🤖 BHANU_GANESH - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask BHANU ...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
