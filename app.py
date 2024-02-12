from flask import Flask,render_template,send_from_directory,request,redirect,flash
from os import path
import backend

app = Flask(__name__,static_folder="static")
app.secret_key = "OURHARDWORKBYTHESEWORDSGUARDEDPLEASEDONTSTEAL"

'''Static page rendering'''
@app.route('/')
def home():
	return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
	if backend.validate_signup(request.form):
		return redirect("/login")
	else:
		return '''<script>alert("Please check whether you have given correct name and email");window.location.href = "/signup";</script>'''

app.run(host="0.0.0.0", port=80, debug=True)