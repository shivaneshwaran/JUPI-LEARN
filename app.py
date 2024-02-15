from flask import Flask,render_template,render_template_string,send_from_directory,request,make_response,redirect
from os import path
import backend

app = Flask(__name__,static_folder="static")



def error_msg(msg):
	return render_template_string("<script>alert('Error: {}');window.history.back();</script>".format(msg))

def display(template,username=""):
	response = make_response(render_template(template,USERNAME=username))
	if template in ("frontendai.html",):
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



'''Static page rendering'''
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(path.join(app.root_path, "static"),"favicon.ico", mimetype="image/vnd.microsoft.icon")

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

@app.route("/course")
def course():
	validated,username = backend.validate_token(request.cookies.get("SESSIONID"))
	if validated:
		return display("frontendai.html",username)
	else:
		return redirect("/login")

@app.route("/logout")
def logout():
	response = make_response(redirect("/login"))
	response.set_cookie("SESSIONID",value="")
	return response



'''Handling POST and GET'''
@app.route('/api_signup', methods=['POST'])
def api_signup():
	validated,message = backend.validate_signup(request.form)
	if validated:
		return render_template_string("<script>alert('Account was successfully created!');window.location.href='/login';</script>")
	else:
		return error_msg(message)

@app.route('/api_signin', methods=['POST'])
def api_signin():
	authenticated,token = backend.signin_account(request.form)
	if authenticated:
		return set_auth_token(token)
	else:
		return error_msg("Invalid username or password!")

app.run(host="0.0.0.0", port=80, debug=True)