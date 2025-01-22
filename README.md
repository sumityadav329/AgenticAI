# AI Agents Hub Web App
![Try Agents Here](https://agenticai-sumityadav329.streamlit.app/)
## Welcome to the AI Agents Hub

The **AI Agents Hub** is a comprehensive platform designed to provide various AI-powered tools and utilities. It includes agents for video summarization, food analysis, code assistance, and chat capabilities. This project leverages the power of Google's Gemini API and is built using Streamlit for a seamless user interface.

## Features

- **Video Summarizer**: Automatically generate summaries of video content.
- **Food Analyzer**: Analyze nutritional information of food items.
- **Code Helper**: Get code suggestions and debugging assistance.
- **Chat Assistant**: Engage in conversation with an AI-powered chatbot.

## Getting Started

### Prerequisites

- **Python 3.10+**: Ensure you have Python installed on your system.
- **Streamlit**: Install Streamlit using pip.
- **Gemini API Key**: Obtain an API key from Google's Gemini service.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/sumityadav329/AgenticAI.git
   cd AgenticAI
   conda create -p venv python=3.10 (or create virtual environment according to ur PC.)
   ```

2. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your Gemini API key:

   ```plaintext
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Streamlit App**

   ```bash
   streamlit run Home.py
   ```

2. **Access the Application**

   Open your web browser and go to `http://localhost:8501` to access the AI Agents Hub.

## Usage

### Video Summarizer

1. Navigate to the "Video Summarizer" tab.
2. Upload a video file.
3. Click "Analyse Video" to get a summary of the video content.

### Food Analyzer

1. Navigate to the "Food Analyzer" tab.
2. Enter the name of a food item.
3. Click "Analyze" to get nutritional information.

### Code Helper

1. Navigate to the "Code Helper" tab.
2. Enter your code snippet or describe the issue.
3. Click "Suitable Options Given" to receive code suggestions or debugging assistance.

### Chat Assistant

1. Navigate to the "Chat Assistant" tab.
2. Start a conversation with the AI-powered chatbot.
3. Ask questions or engage in general conversation.

## Acknowledgements

- **Google**: For providing the Gemini API.
- **Streamlit**: For creating the web application interface.
- **phidata**: For additional resources and support.

## Contact

- **Email**: [sumityadav@gmail.com](mailto:sumityadav@gmail.com)
- **GitHub**: [Sumit Yadav](https://github.com/sumityadav329)
- **Buy Me a Coffee**: [Support Sumit Yadav](https://buymeacoffee.com/sumityadav)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
