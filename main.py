from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import logging
import anthropic
from anthropic import APIError

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all for testing

# API key setup - Using Anthropic API key
os.environ["ANTHROPIC_API_KEY"] = ""

print("Environment setup complete. Anthropic API key configured.")

class PromptEnhancer:
    FALLBACK_TEMPLATE = """
    You are an AI assistant tasked with the following:

    Task: {task}

    Requirements:
    - Provide detailed and accurate information
    - Use clear, professional language
    - Include practical examples where relevant
    - Structure the response logically
    - Ensure the output is actionable and optimized for clarity
    """
    
    def __init__(self):
        self.anthropic_client = None
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=api_key)
                logger.info("Anthropic client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")
        else:
            logger.error("Anthropic API key not found in environment variables")
    
    def enhance_with_llm(self, original_prompt, source_platform=None):
        enhancement_prompt = f"""You are an expert prompt engineer. Your task is to enhance the following prompt, originally from {source_platform or 'an unknown platform'}, to make it more effective for AI interactions.

Original Prompt: {original_prompt}

Please provide an enhanced version that:
1. Adds clear context and background based on the source platform
2. Specifies the desired output format as a structured JSON
3. Includes relevant constraints and requirements
4. Makes the intent crystal clear
5. Adds helpful examples if needed
6. Enhances prompts of any length, optimizing for clarity and detail

Return only the enhanced prompt text, nothing else."""

        try:
            if self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",  # Updated to latest Claude model
                    max_tokens=1500,  # Increased to handle prompts of any length
                    temperature=0.5,
                    messages=[{
                        "role": "user",
                        "content": enhancement_prompt
                    }]
                )
                return response.content[0].text.strip()
            else:
                logger.warning("Anthropic client not available, using fallback")
                return self.fallback_enhancement(original_prompt)
        except APIError as e:
            logger.error(f"LLM Enhancement failed: {e}")
            return self.fallback_enhancement(original_prompt)
        except Exception as e:
            logger.error(f"Unexpected error during enhancement: {e}")
            return self.fallback_enhancement(original_prompt)
    
    def fallback_enhancement(self, original_prompt):
        return self.FALLBACK_TEMPLATE.format(task=original_prompt).strip()
    
    def generate_json_structure(self, enhanced_prompt, original_prompt):
        return {
            "task": {
                "original_prompt": original_prompt,
                "enhanced_prompt": enhanced_prompt
            }
        }

enhancer = PromptEnhancer()

@app.route('/')
def serve_frontend():
    """Serve the main HTML file"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return """
        <h1>Frontend file not found</h1>
        <p>Please ensure 'index.html' is in the same directory as main.py</p>
        <p>Current directory: {}</p>
        <p>Files in directory: {}</p>
        """.format(os.getcwd(), os.listdir('.')), 404

@app.route('/capture', methods=['POST'])
def capture_prompt():
    """Capture a prompt from an external platform and enhance it"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400
        original_prompt = data['prompt'].strip()
        if not original_prompt:
            return jsonify({'error': 'Empty prompt provided'}), 400
        
        source_platform = data.get('source_platform', 'unknown')
        enhanced_prompt = enhancer.enhance_with_llm(original_prompt, source_platform)
        json_structure = enhancer.generate_json_structure(enhanced_prompt, original_prompt)
        
        return jsonify(json_structure)
    except Exception as e:
        logger.error(f"Capture failed: {str(e)}")
        return jsonify({'error': f'Capture failed: {str(e)}'}), 500

@app.route('/test-claude', methods=['GET'])
def test_claude():
    """Test endpoint to verify Claude API is working"""
    try:
        if enhancer.anthropic_client:
            test_response = enhancer.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=[{
                    "role": "user",
                    "content": "Please respond with 'Claude API is working correctly!' and nothing else."
                }]
            )
            return jsonify({
                "status": "success",
                "message": "Claude API is connected and working",
                "response": test_response.content[0].text
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Claude API client not initialized"
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Claude API test failed: {str(e)}"
        })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "llm_available": {
            "anthropic": enhancer.anthropic_client is not None
        }
    })

if __name__ == '__main__':
    logger.info("Starting Prompt Enhancer API...")
    logger.info(f"Anthropic: {'✓' if enhancer.anthropic_client else '✗'}")
    app.run(debug=True, host='0.0.0.0', port=5000)