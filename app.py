# !/usr/bin/python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template("JUPILEARNINGWEBAPP.HTML")
if __name__ == '__main__':
   app.run(host="0.0.0.0",port=80,debug=True)