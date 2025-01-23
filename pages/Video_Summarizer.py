import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai
import time
from pathlib import Path
import tempfile
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoSummarizerApp:
    def __init__(self):
        self.setup_environment()
        self.setup_constants()
        self.setup_ui()
        
    def setup_environment(self):
        """Initialize environment variables and API configuration"""
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        
    def setup_constants(self):
        """Set up application constants"""
        self.MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
        self.ALLOWED_EXTENSIONS = ['mp4', 'mov', 'avi']
        
    def setup_ui(self):
        """Configure the user interface"""
        st.title("🎥 Video AI Summarizer")
        st.header("Powered by Gemini 2.0")
        
        # Add custom styling
        st.markdown("""
            <style>
            .upload-container {
                border: 2px dashed #cccccc;
                border-radius: 5px;
                padding: 20px;
                text-align: center;
                margin: 20px 0;
            }
            .stProgress > div > div > div {
                background-color: #00a67e;
            }
            .analysis-container {
                background-color: #252536;
                border-radius: 15px;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
                font-family: 'Arial', sans-serif;
                padding: 20px;
                margin-top: 20px;
            }
            .analysis-title {
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .analysis-text {
                font-size: 1em;
            }
            </style>
        """, unsafe_allow_html=True)

        # Sidebar information
        with st.sidebar:
            st.header("How It Works")
            st.write("""
            1. Upload a video file
            2. Our AI will analyze the video content
            3. Get a detailed summary and analysis
            """)
            st.info("📹 Best results with clear, well-encoded video files")

    @staticmethod
    @st.cache_resource
    def initialize_agent():
        """Initialize the AI agent with caching"""
        return Agent(
            name="Video AI Summarizer",
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[DuckDuckGo()],
            markdown=True,
        )

    def validate_video(self, video_file):
        """Validate the uploaded video file"""
        if video_file.size > self.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds {self.MAX_FILE_SIZE / 1024 / 1024}MB limit")
            
        extension = video_file.name.split('.')[-1].lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(f"Invalid file format. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}")
            
        return True

    def process_video(self, video_file, query):
        """Process the video and generate analysis"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
                temp_video.write(video_file.read())
                video_path = temp_video.name

            # Update progress
            progress_bar.progress(0.2)
            status_text.text("Uploading video...")
            processed_video = genai.upload_file(video_path)

            # Process video
            progress_bar.progress(0.4)
            status_text.text("Processing video...")
            while processed_video.state.name == "PROCESSING":
                time.sleep(1)
                processed_video = genai.get_file(processed_video.name)

            # Generate analysis
            progress_bar.progress(0.7)
            status_text.text("Analyzing content...")
            
            analysis_prompt = f"""
            Analyze the uploaded video for content and context.
            Query: {query}
            
            Provide a detailed response with:
            1. Main points and key moments
            2. Relevant timestamps
            3. Context and insights
            4. Summary and recommendations
            """

            agent = self.initialize_agent()
            response = agent.run(analysis_prompt, videos=[processed_video])

            # Complete analysis
            progress_bar.progress(1.0)
            status_text.text("Analysis complete!")
            
            return response.content

        except Exception as e:
            logger.error(f"Error during video processing: {e}")
            return f"Error analyzing video: {str(e)}"
        finally:
            # Cleanup
            if 'video_path' in locals():
                Path(video_path).unlink(missing_ok=True)

    def run(self):
        """Main application loop"""
        try:
            # Main content area
            col1, col2 = st.columns([1, 2])  # Adjust column widths

            with col1:
                st.header("Upload Video")
                video_file = st.file_uploader(
                    "Upload a video file",
                    type=self.ALLOWED_EXTENSIONS,
                    help=f"Maximum size: {self.MAX_FILE_SIZE / 1024 / 1024}MB"
                )

                if video_file:
                    if self.validate_video(video_file):
                        st.video(video_file)

            with col2:
                st.header("Video Analysis")
                if video_file:
                    query = st.text_area(
                        "What would you like to know about this video?",
                        placeholder="Example: 'Summarize the main points' or 'Analyze the speaker's tone'",
                        height=100
                    )
                    
                    if st.button("🔍 Analyze & Summarizer Video", type="primary"):
                        if query:
                            with st.spinner("Processing video..."):
                                analysis = self.process_video(video_file, query)
                                
                                # Display analysis below the video (full width)
                                st.markdown("""
                                <div class="analysis-container">
                                    <div class="analysis-title">📊 Video Analysis</div>
                                    <div class="analysis-text">
                                """, unsafe_allow_html=True)
                                
                                st.markdown(analysis, unsafe_allow_html=True)
                                
                                st.markdown("</div></div>", unsafe_allow_html=True)
                                st.caption(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        else:
                            st.warning("Please enter a question or analysis prompt.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def main():
    app = VideoSummarizerApp()
    app.run()

if __name__ == "__main__":
    main()