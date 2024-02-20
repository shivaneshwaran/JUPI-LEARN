from flask import Flask, render_template, render_template_string, send_from_directory, request, make_response, redirect, jsonify
from os import path
import requests
import backend


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



@app.route("/logout")
def logout():
    response = make_response(redirect("/login"))
    response.set_cookie("SESSIONID", value="")
    return response


@app.route("/course", methods=["POST", "GET"])
def course():
    try:
        course = request.form["course"]
    except:
        course = "Nothing"
        
    validated, username = backend.validate_token(request.cookies.get("SESSIONID"))
    
    if validated:
        # Make a request to the frontend server to fetch frontend.html
        frontend_url = "http://frontend_server_address:port/frontend.html"
        response = requests.get(frontend_url)
        
        if response.status_code == 200:
            # If the request is successful, return the HTML content
            return response.text
        else:
            # Handle the case where the request to frontend fails
            return "Error: Failed to fetch frontend.html"
    else:
        return redirect("/404")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1983, debug=True)
