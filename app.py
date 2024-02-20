from flask import Flask, render_template, send_from_directory, request, redirect, flash, jsonify
from os import path
import mysql.connector as mys
import re
import hashlib
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
app.secret_key = "OURHARDWORKBYTHESEWORDSGUARDEDPLEASEDONTSTEAL"
CORS(app)

#Global variables and configuration for the database
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "changE me p1ease!"
MYSQL_DB = "JUPI"

# Configure Generative AI with your API key
genai.configure(api_key="your_api_key_here")

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

'''Static page rendering'''
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/course")
def course():
    return render_template("frontendai.html")

'''Handling POST and GET'''
@app.route('/api_signup', methods=['POST'])
def api_signup():
    if validate_signup(request.form):
        return redirect("/login")
    else:
        return '''<script>alert("Please check whether you have given correct name and email");window.location.href = "/signup";</script>'''

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    history = data.get('history', [])
    user_input = data.get('user_input', 'hello')  # Default to 'hello' if no input is provided

    convo = model.start_chat(history=history)
    convo.send_message(user_input)
    response = convo.last.text

    return jsonify({'response': response})

def validate_signup(data):
    '''Validates signup information provided by the user'''
    errors = []
    #Name
    if not str(data["name"]).replace(" ","SEPchar").isalpha():
        errors.append("Name should only contain alphabets!")
    #Email
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(emailRegex,data["email"]):
        errors.append("Invalid email!")
    #Password
    password = hashlib.sha256(str(data["password"]).encode("UTF-8"))
    '''Call create account here'''

    if errors == []:
        return True
    else:
        return False

# Initialize MySQL DB and perform other database operations as needed

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1983, debug=True)
