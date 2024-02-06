from flask import Flask,render_template,send_from_directory
from os import path

app = Flask(__name__,static_folder="static")

@app.route('/home')
def home():
    return render_template("JUPILEARNINGWEBAPP.HTML")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
