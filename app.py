from flask import Flask, render_template, render_template_string, send_from_directory, request, make_response, redirect, jsonify
from os import path
import requests
import backend
import google.generativeai as genai

app = Flask(__name__, static_folder="static")

def error_msg(msg):
    return render_template_string("<script>alert('Error: {}');window.history.back();</script>".format(msg))

def display(template, username="", course="Nothing"):
    response = make_response(render_template(template, USERNAME=username, COURSE=course))
    response.headers["Cache-Control"] = "no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    if request.cookies.get("SESSIONID") is None:
        response.set_cookie("SESSIONID", value="")
    return response

def set_auth_token(token):
    response = make_response(redirect("/course"))
    response.set_cookie("SESSIONID", value=token)
    return response

'''Static page rendering'''
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, "static"), "favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.route('/')
def home():
    return display("index.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.route("/about")
def about():
    return display("about.html")

@app.route("/login")
def login():
    if backend.validate_token(request.cookies.get("SESSIONID"))[0]:
        return redirect("/course")
    else:
        return display("login.html")

@app.route("/signup")
def signup():
    return display("signup.html")

@app.route("/course", methods=["POST", "GET"])
def course():
    try:
        course = request.form["course"]
    except:
        course = "Nothing"
    
    validated, username = backend.validate_token(request.cookies.get("SESSIONID"))
    
    if validated:
        # If the user is authenticated, render the frontend AI page
        return render_template("frontendai.html")
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect("/login")


@app.route("/logout")
def logout():
    response = make_response(redirect("/login"))
    response.set_cookie("SESSIONID", value="")
    return response

'''Handling Authentication'''
@app.route("/api_signup", methods=["POST"])
def api_signup():
    validated, message = backend.validate_signup(request.form)
    if validated:
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
    else:
        return error_msg(message)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    history = data.get('history', [])
    user_input = data.get('user_input', 'hello')  # Default to 'hello' if no input is provided

    convo = model.start_chat(history=history)
    convo.send_message(user_input)
    response = convo.last.text

    return jsonify({'response': response})

@app.route("/api_signin", methods=["POST"])
def api_signin():
    authenticated, token = backend.signin_account(request.form)
    if authenticated:
        return set_auth_token(token)
    else:
        return error_msg("Invalid username or password!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1983, debug=True)
