🚀 Prompt-to-JSON Enhancer

A Flask-based API that captures raw prompts, enhances them using Claude API (Anthropic), and outputs structured JSON format for optimized AI interactions.

⚠️ Note: Claude API access quota is finished, so further live testing is paused.

✨ Features

🌐 Flask backend with REST APIs

🔄 CORS enabled for cross-platform integration

📝 Logging & Health-check endpoints

🤖 Claude 3.5 Sonnet (Anthropic API) for prompt enhancement

📦 Structured JSON output generation

📂 Project Structure
├── main.py          # Flask app with endpoints
├── index.html       # Frontend (if any UI added)
├── requirements.txt # Dependencies
└── README.md        # Project documentation

⚙️ Installation
# Clone the repo
git clone https://github.com/your-username/prompt-to-json-enhancer.git
cd prompt-to-json-enhancer

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

🚀 Usage

Set up Anthropic API key

export ANTHROPIC_API_KEY="your_api_key_here"


Run the server

python main.py


API Endpoints

/capture → Capture and enhance a prompt

/test-claude → Test Claude API connection

/health → Health check

📌 Example

Input Prompt (POST /capture):

{
  "prompt": "Build a Flask API for todo management",
  "source_platform": "LinkedIn"
}


Enhanced Output:

{
  "task": {
    "original_prompt": "Build a Flask API for todo management",
    "enhanced_prompt": "You are an expert backend developer. Create a Flask API for todo management with JWT authentication, CRUD operations, logging, and return all responses in JSON format."
  }
}

🔮 Future Improvements

Add OpenAI API integration as fallback

Extend support for multiple LLM providers

Build a simple frontend UI for testing

🏷️ Tech Stack

Python (Flask)

Anthropic Claude API

REST APIs

Logging

✍️ Developed by Azaz Ur Rehman
📌 
