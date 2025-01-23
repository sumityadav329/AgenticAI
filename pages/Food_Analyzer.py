import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

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

# Configure Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Maximum file size allowed (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

class FoodAnalyzer:
    def __init__(self):
        # Set up Streamlit app configuration
        st.set_page_config(
            page_title="Food Analyzer",
            page_icon="🍽️",
            layout="wide"
        )
        # Define the input prompt for the Gemini API
        self.input_prompt = """
        You are an expert nutritionist and food analyst. Carefully examine the food image and provide:
        1. Detailed list of food items identified
        2. Calories for each item
        3. Nutritional breakdown (protein, carbs, fats)
        4. Estimated total calorie count
        5. Brief health insights or recommendations

        Format your response clearly with headings and bullet points.
        """

    @staticmethod
    def process_uploaded_image(uploaded_file):
        """Process uploaded image into a format suitable for the Gemini API."""
        if uploaded_file is not None:
            # Check file size
            if uploaded_file.size > MAX_FILE_SIZE:
                raise ValueError(f"File size exceeds the limit of 10 MB. Uploaded file size: {uploaded_file.size / (1024 * 1024):.2f} MB")
            
            bytes_data = uploaded_file.getvalue()
            return [
                {
                    "mime_type": uploaded_file.type,  # Get MIME type of uploaded file
                    "data": bytes_data
                }
            ]
        else:
            raise FileNotFoundError("No file uploaded")

    @staticmethod
    def get_gemini_response(image_data, prompt):
        """Send image and prompt to the Gemini API and return the response."""
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")
        response = model.generate_content([image_data[0], prompt])
        return response.text

    def render(self):
        # Title and description
        st.title("🍽️ AI Food Analyzer")
        st.markdown("*Upload a photo of your meal and get detailed nutritional insights!*")

        # Sidebar
        with st.sidebar:
            st.header("How It Works")
            st.write("""
            1. Upload a clear image of your food
            2. Our AI will analyze the image
            3. Receive detailed nutritional information
            """)
            st.info("Best results with clear, well-lit food images")

        # Main content area
        col1, col2 = st.columns([1, 2])  # Adjust column widths

        with col1:
            st.header("Upload Image")
            # Image Upload
            uploaded_file = st.file_uploader(
                "Choose a food image (max 10 MB)",
                type=['jpg', 'jpeg', 'png'],
                help="Upload a clear image of your meal (max 10 MB)"
            )
            # Display uploaded image
            if uploaded_file is not None:
                try:
                    # Check file size
                    if uploaded_file.size > MAX_FILE_SIZE:
                        st.error(f"File size exceeds the limit of 10 MB. Uploaded file size: {uploaded_file.size / (1024 * 1024):.2f} MB")
                    else:
                        image = Image.open(uploaded_file)
                        st.image(image, caption="Uploaded Image", use_container_width=True)
                except Exception as e:
                    st.error(f"Error processing image: {e}")

        with col2:
            st.header("Food Analysis")
            if uploaded_file:
                with st.spinner('Analyzing your meal...'):
                    try:
                        # Process image and get analysis result
                        image_data = self.process_uploaded_image(uploaded_file)
                        analysis_result = self.get_gemini_response(image_data, self.input_prompt)

                        # Display analysis result below the image (full width)
                        st.markdown("### Analysis Result")
                        st.markdown(analysis_result)
                    except ValueError as ve:
                        st.error(str(ve))
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

def main():
    try:
        analyzer = FoodAnalyzer()
        analyzer.render()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error("An unexpected error occurred. Please refresh and try again.")

# Run the app if executed as the main file
if __name__ == "__main__":
    main()