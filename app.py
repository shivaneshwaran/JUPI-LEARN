from flask import Flask,render_template,render_template_string,send_from_directory,request,make_response
from os import path
import backend

app = Flask(__name__,static_folder="static")

'''Static page rendering'''
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
	response = make_response(render_template("index.html"))
	if request.cookies.get("SESSIONID") is None:
		response.set_cookie("SESSIONID",value="0")
	return response

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
	validated,message = backend.validate_signup(request.form)
	if validated:
		return render_template_string("<script>alert('Account was successfully created!');window.location.href='/login';</script>")
	else:
		return render_template_string("<script>alert('Error: {}');window.history.back();</script>".format(message))

def api_signin():
	pass

app.run(host="0.0.0.0", port=80, debug=True)