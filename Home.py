import streamlit as st
import importlib
from pages import Video_Summarizer, Food_Analyzer, Code_Helper, Chat_Assistant
import logging
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log to a file
    filemode='a'  # Append mode
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables")
    st.error("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Set page configuration
st.set_page_config(
    page_title="AI Agents Hub",
    page_icon="🤖",
    layout="wide"
)

# Sidebar Navigation
sidebar_options = {
    "Video Summarizer": "Video_Summarizer",
    "Food Analyzer": "Food_Analyzer",
    "Code Helper": "Code_Helper",
    "Chat Assistant": "Chat_Assistant",

}

# Main Application Logic
def main():

    st.title("Welcome to the home page of AI Agents Hub.")
    st.subheader("⬅ Click and Choose Any Agent from the left ⬅ ")
    # Footer
    st.markdown("""
    <div class="app-footer">
        <p>Made with ❤️ by <a href="https://buymeacoffee.com/sumityadav" target="_blank">Sumit Yadav</a></p>
        <p>Acknowledgements: Google, Streamlit, and phidata</p>
        <p>Contact: <a href="mailto:sumityadav329@gmail.com">sumityadav329@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)
# Run the app
if __name__ == "__main__":
    main()
