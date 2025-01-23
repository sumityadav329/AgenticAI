import streamlit as st
import google.generativeai as genai
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
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if not api_key:
        st.error("API key is required to proceed.")
        st.stop()
genai.configure(api_key=api_key)

# Maximum chat history length
MAX_HISTORY_LENGTH = 20

class GeminiChatbot:
    def __init__(self):
        self.initialize_chat()
        self.setup_streamlit()

    def initialize_chat(self):
        """Initialize the chat session and state."""
        try:
            self.model = genai.GenerativeModel(model_name="gemini-pro")
            self.chat = self.model.start_chat(history=[])
            if "gemini_chat_history" not in st.session_state:
                st.session_state["gemini_chat_history"] = []
        except Exception as e:
            logger.error(f"Error initializing chat: {e}")
            st.error("Failed to start chat session.")

    def setup_streamlit(self):
        """Configure Streamlit page layout."""
        st.title("💬 Gemini AI Chatbot")
        st.markdown("""
            **Welcome to the Gemini AI Chatbot!**  
            Ask any question, and our advanced Gemini model will respond in real-time.  
            Your conversation history is preserved during the session.
        """)
        # Inform users about chat history
        st.info("""
            **Note:** This is a demo chat app using the Gemini API.  
            - Your chat history will last only during this session.  
            - We do not save your chat history permanently.  
            - The chat history is limited to the last 20 messages to ensure smooth performance.
        """)
        # Sidebar information
        with st.sidebar:
            st.header("How It Works")
            st.write("""
            1. Ask a question or provide a prompt
            2. Our AI will understand and respond
            3. Get helpful answers and insights
            """)
            st.info("💬 Best results with clear, concise questions and prompts")

    def get_gemini_response(self, query):
        """Get streaming response from Gemini API."""
        try:
            return self.chat.send_message(query, stream=True)
        except Exception as e:
            logger.error(f"Error fetching response from Gemini API: {e}")
            st.error(f"Failed to fetch response: {str(e)}")
            return None

    def display_chat_history(self):
        """Display the chat conversation history."""
        st.divider()
        st.subheader("Conversation History")

        # Display chat history in order (newest at the bottom)
        for role, message in st.session_state["gemini_chat_history"]:
            message_container = st.chat_message("user" if role == "user" else "assistant")
            message_container.markdown(
                f"**{'You' if role == 'user' else 'Gemini'}:** {message}"
            )

    def handle_user_input(self):
        """Handle user input and generate responses."""
        st.divider()

        # Input field at the bottom
        user_input = st.chat_input(
            "Type your query below and press Enter to send:",
            key="user_input"
        )

        # If the user presses Enter or clicks a button
        if user_input and user_input.strip():
            if len(user_input.strip()) > 1000:
                st.warning("Query is too long. Please keep it under 1000 characters.")
            else:
                # Add user query to chat history
                st.session_state["gemini_chat_history"].append(("user", user_input))
                # Trim history if it exceeds the maximum length
                if len(st.session_state["gemini_chat_history"]) > MAX_HISTORY_LENGTH:
                    st.session_state["gemini_chat_history"] = st.session_state["gemini_chat_history"][-MAX_HISTORY_LENGTH:]
                st.chat_message("user").markdown(f"**You:** {user_input}")

                # Generate and display Gemini response
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    with st.spinner("Generating response..."):
                        response_stream = self.get_gemini_response(user_input)

                    if response_stream:
                        bot_response = ""
                        try:
                            for chunk in response_stream:
                                bot_response += chunk.text
                                placeholder.markdown(f"**Gemini:** {bot_response}")
                            st.session_state["gemini_chat_history"].append(("bot", bot_response))
                        except Exception as e:
                            logger.error(f"Error processing streaming response: {e}")
                            st.error("An error occurred while processing the response.")

        # New Chat button
        if st.button("New Chat", key="new_chat", use_container_width=True):
            self.initialize_chat()  # Reinitialize the chat session
            st.success("Started a new chat session. Previous history is retained.")

def main():
    """Main application entry point."""
    try:
        chatbot = GeminiChatbot()
        chatbot.display_chat_history()
        chatbot.handle_user_input()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error("An unexpected error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()