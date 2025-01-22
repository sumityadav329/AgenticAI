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
    logger.error("GEMINI_API_KEY not found in environment variables")
    st.error("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=api_key)

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
        except ModuleNotFoundError:
            logger.error(f"Module not found error: {e}")
            st.error(f"Module not found error: {str(e)}")
        except ImportError as import_err:
            logger.error(f"Import error: {import_err}")
            st.error(f"Import error: {str(import_err)}")
        except AttributeError as attr_err:
            logger.error(f"Attribute error: {attr_err}")
            st.error(f"Attribute error: {str(attr_err)}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            st.error(f"An unexpected error occurred: {str(e)}")
        return None

    def display_chat_history(self):
        """Display the chat conversation history."""
        st.divider()
        st.subheader("Conversation History")
        
        for role, message in st.session_state["gemini_chat_history"]:
            message_container = st.chat_message("user" if role == "user" else "assistant")
            message_container.markdown(
                f"**{'You' if role == 'user' else 'Gemini'}:** {message}"
            )

    def handle_user_input(self):
        """Handle user input and generate responses."""
        st.divider()
        user_input = st.text_input(
            "Type your query below:",
            key="user_input",
            placeholder="Ask me anything..."
        )
        
        col1, col2 = st.columns([6, 1])
        with col1:
            submit_query = st.button("Ask", key="submit_query", use_container_width=True)
        with col2:
            if st.button("Clear", key="clear_chat", use_container_width=True):
                st.session_state["gemini_chat_history"] = []
                st.experimental_rerun()

        if submit_query and user_input.strip():
            st.session_state["gemini_chat_history"].append(("user", user_input))
            st.chat_message("user").markdown(f"**You:** {user_input}")

            with st.chat_message("assistant"):
                placeholder = st.empty()
                response_stream = self.get_gemini_response(user_input)
                
                if response_stream:
                    bot_response = ""
                    for chunk in response_stream:
                        bot_response += chunk.text
                        placeholder.markdown(f"**Gemini:** {bot_response}")
                    
                    st.session_state["gemini_chat_history"].append(("bot", bot_response))

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