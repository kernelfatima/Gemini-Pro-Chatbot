import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon="🤖",  # Favicon emoji
    layout="centered"  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure API key is loaded
if not GOOGLE_API_KEY:
    st.error("API Key missing! Please check your .env file.")
else:
    gen_ai.configure(api_key=GOOGLE_API_KEY)

# Set up Google Gemini AI model (Verify model name using list_models)
model = gen_ai.GenerativeModel("gemini-1.5-pro")  # Adjust based on supported models

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title
st.title("🤖 Gemini Pro - ChatBot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        assistant_response = gemini_response.text if hasattr(gemini_response, "text") else "Error: No response received."

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    except Exception as e:
        st.error(f"Error communicating with Gemini-Pro: {e}")
