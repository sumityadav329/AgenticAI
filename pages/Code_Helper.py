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

class CodeHelper:
    def __init__(self):
        self.model = genai.GenerativeModel(model_name="gemini-pro")
        self.chat = self.model.start_chat(history=[])
        self.initialize_session_state()
        self.setup_ui()

    def initialize_session_state(self):
        if "code_helper_chat_history" not in st.session_state:
            st.session_state["code_helper_chat_history"] = []

    def setup_ui(self):
        st.title("💻 AI Code Explainer & Debugger")
        st.markdown("""
            **Welcome to the AI Code Helper!**  
            Paste your code snippet below, and our advanced AI will help you understand, debug, or optimize it.
        """)
        # Sidebar information
        with st.sidebar:
            st.header("How It Works")
            st.write("""
            1. Enter your code snippet or question
            2. Our AI will analyze the code
            3. Get suggestions, explanations, and solutions
            """)
            st.info("💻 Best results with clear, concise code snippets")

    def get_gemini_response(self, query):
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

    def handle_code_analysis(self):
        code_snippet = st.text_area(
            "Paste your code snippet below:",
            height=200,
            placeholder="def example():\n    return 'Hello, World!'"
        )

        task = st.radio(
            "What would you like the AI to do?",
            options=["Explain the Code", "Debug the Code", "Optimize the Code"],
            horizontal=True
        )

        if st.button("Analyze Code", type="primary"):
            if code_snippet.strip():
                self.process_code(code_snippet, task)
            else:
                st.warning("Please paste some code to analyze.")

    def process_code(self, code_snippet, task):
        user_task = f"Task: {task}\nCode:\n{code_snippet}"
        st.session_state["code_helper_chat_history"].append(("user", user_task))
        
        with st.spinner(f"{task}ing your code..."):
            prompt = self.create_analysis_prompt(task, code_snippet)
            response_stream = self.get_gemini_response(prompt)
            
            if response_stream:
                response = self.display_streaming_response(response_stream)
                st.session_state["code_helper_chat_history"].append(("bot", response))

    @staticmethod
    def create_analysis_prompt(task, code):
        task_prompts = {
            "Explain the Code": "Explain this code in detail, including its purpose, functionality, and key concepts:",
            "Debug the Code": "Analyze this code for potential issues and provide debugging suggestions:",
            "Optimize the Code": "Suggest optimizations for this code, explaining the improvements:"
        }
        return f"{task_prompts[task]}\n\n{code}"

    def display_streaming_response(self, stream):
        response_container = st.empty()
        full_response = ""
        
        for chunk in stream:
            full_response += chunk.text
            response_container.markdown(f"**CodeHelper:** ```python\n{full_response}\n```")
        
        return full_response

    def display_chat_history(self):
        st.divider()
        st.subheader("Analysis History")
        
        for role, message in st.session_state["code_helper_chat_history"]:
            message_container = st.chat_message("user" if role == "user" else "assistant")
            message_container.markdown(f"**{'You' if role == 'user' else 'CodeHelper'}:** ```python\n{message}\n```")

def main():
    try:
        helper = CodeHelper()
        helper.handle_code_analysis()
        helper.display_chat_history()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error("An unexpected error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()