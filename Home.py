import streamlit as st
import logging
import importlib
from pages import Video_Summarizer, Food_Analyzer, Code_Helper, Chat_Assistant
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

# Set page configuration
st.set_page_config(
    page_title="AI Agents Hub",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for API key
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = None

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables")
    st.error("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Custom CSS for styling
st.markdown("""
    <style>
    .hero {
        background-color: #0e1117;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 3rem;
        color: #ffffff;
    }
    .hero p {
        font-size: 1.2rem;
        color: #cccccc;
    }
    .cta-button {
        background-color: #00a67e;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-align: center;
        margin: 1rem auto;
        width: fit-content;
    }
    .cta-button:hover {
        background-color: #008c6a;
    }
    .app-footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #cccccc;
        color: #666666;
    }
    .app-footer a {
        color: #00a67e;
        text-decoration: none;
    }
    .app-footer a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🚀 AI Agents Hub")


# API Key Input in Sidebar
st.sidebar.markdown("### API Key Settings")

# Link to get API key
st.sidebar.markdown("""
    <div style="font-size: 0.9em; color: #666666; margin-bottom: 10px;">
        Don't have an API key? <a href="https://aistudio.google.com/app/apikey" target="_blank">Get one for free</a>.
    </div>
""", unsafe_allow_html=True)

user_api_key = st.sidebar.text_input(
    "Enter your Gemini API Key (optional):",
    type="password",
    help="If the default API key stops working, you can provide your own."
)

# Transparency Message
st.sidebar.markdown("""
    <div style="font-size: 0.9em; color: #666666; margin-top: 10px;">
        <b>Transparency Note:</b><br>
        - We do <b>not save</b> your API key permanently.<br>
        - Your API key is <b>not visible</b> to anyone, including us.<br>
        - It is used only for the current session.
    </div>
""", unsafe_allow_html=True)

# Save API key to session state
if user_api_key:
    st.session_state.user_api_key = user_api_key
    st.sidebar.success("API key saved successfully!")
elif st.session_state.user_api_key:
    st.sidebar.info("Using saved API key.")
else:
    st.sidebar.warning("No API key provided. Using default key.")

# Main Application Logic
def main():
    # Hero Section
    st.markdown("""
        <div class="hero">
            <h1>AI Agents Hub</h1>
            <p>Your one-stop solution for AI-powered tools. Explore our agents to analyze, summarize, and assist with your tasks.</p>
            <div class="cta-button">⬅ Choose an Agent from the Sidebar</div>
        </div>
    """, unsafe_allow_html=True)

    # Introduction Section
    st.markdown("""
        ### What is AI Agents Hub?
        AI Agents Hub is a collection of intelligent tools powered by **Google Gemini** and **Streamlit**. 
        Each agent is designed to help you with specific tasks, such as summarizing videos, analyzing food, debugging code, or chatting with an AI assistant.
    """)

    # Features Section
    st.markdown("""
        ### Features
        - **🎥 Video Summarizer**: Get detailed summaries and insights from your videos.
        - **🍽️ Food Analyzer**: Analyze food images for nutritional information.
        - **💻 Code Helper**: Debug, explain, and optimize your code snippets.
        - **💬 Chat Assistant**: Chat with an AI-powered assistant for quick answers.
    """)

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