from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import google.generativeai as genai
from functools import wraps
import backend

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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is authenticated
        if not backend.validate_token(request.cookies.get("SESSIONID"))[0]:
            # Redirect the user to the login page if not authenticated
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login")
def login():
    if backend.validate_token(request.cookies.get("SESSIONID"))[0]:
        return redirect("/auth")
    else:
        return redirect ("https://jupilearning.app/login")
    
@app.route('/')
@login_required
def index():
    return render_template('frontendai.html')

@app.route("/about")
def about():
    return redirect('https://jupilearning.app/about')

@app.route('/home')
def home():
    return redirect('https://jupilearning.app')

@app.route('/logout')
def logout():
    return redirect('https://jupilearning.app')

@app.route("/auth", methods=["POST","GET"])
def auth():
    try:
        auth = request.form["course"]
    except:
        auth = "Nothing"
    validated, username = backend.validate_token(request.cookies.get("SESSIONID"))
    if validated:
        return redirect("/")
    else:
        return redirect("/login")

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
