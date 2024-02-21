from flask import Flask, request, jsonify, render_template, redirect,make_response,render_template_string,send_from_directory,request
from flask_cors import CORS
import google.generativeai as genai
from functools import wraps
import backend
from os import path

app = Flask(__name__,static_folder="static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

# Configure Generative AI with your API key
genai.configure(api_key="AIzaSyDkYqYhYt3d6t63VgMJRgJby7bZJ5KViXc")

# Set up your conversational model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 20000,
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

def error_msg(msg):
	return render_template_string("<script>alert('Error: {}');window.history.back();</script>".format(msg))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is authenticated
        if not backend.validate_token(request.cookies.get("SESSIONID"))[0]:
            # Redirect the user to the login page if not authenticated
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
def display(template,username="",course="Nothing"):
	response = make_response(render_template(template,USERNAME=username,COURSE=course))
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "0"
	if request.cookies.get("SESSIONID") is None:
		response.set_cookie("SESSIONID",value="")
	return response
def set_auth_token(token):
	response = make_response(redirect("/course"))
	response.set_cookie("SESSIONID",value=token)
	return response

@app.route("/login")
def login():
	if backend.validate_token(request.cookies.get("SESSIONID"))[0]:
		return redirect("/course")
	else:
		return display("login.html")
    
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

@app.route("/course",methods=["POST","GET"])
def course():
	try:
		course = request.form["course"]
	except:
		course = "Nothing"
	validated,username = backend.validate_token(request.cookies.get("SESSIONID"))
	if validated:
		return redirect("/")
	else:
		return redirect("/login")


@app.route("/signup")
def signup():
	return display("signup.html")

'''Handling Authentication'''
@app.route("/api_signup", methods=["POST"])
def api_signup():
	validated,message = backend.validate_signup(request.form)
	if validated:
		return render_template_string("<script>alert('Account was successfully created!');window.location.href='/login';</script>")
	else:
		return error_msg(message)

@app.route("/api_signin", methods=["POST"])
def api_signin():
	authenticated,token = backend.signin_account(request.form)
	if authenticated:
		return set_auth_token(token)
	else:
		return error_msg("Invalid username or password!")
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
