from flask import Flask, render_template

app = Flask(__name__,static_folder="static")

@app.route('/')
def home():
    return render_template("JUPILEARNINGWEBAPP.HTML")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)