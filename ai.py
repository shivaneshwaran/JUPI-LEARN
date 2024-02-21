from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import backend
import requests

app = Flask(__name__)
CORS(app)

# Configure Generative AI with your API key
genai.configure(api_key="AIzaSyDkYqYhYt3d6t63VgMJRgJby7bZJ5KViXc")

# Set up your conversational model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
                    
                
@app.route("/login")
def login():
	if backend.validate_token(request.cookies.get("SESSIONID"))[0]:
		return index
	else:
		return display("login.html")
@app.route('/')
def index():
    return render_template('frontendai.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    history = data.get('history', [])
    user_input = data.get('user_input', 'hello')  # Default to 'hello' if no input is provided

    convo = model.start_chat(history=history)
    convo.send_message(user_input)
    response = convo.last.text

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
