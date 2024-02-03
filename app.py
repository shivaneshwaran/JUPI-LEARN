# !/usr/bin/python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_templates("JUPILEARNINGWEBAPP.HTML")

@app.route('/about')
def about():
    return render_templates("about.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
