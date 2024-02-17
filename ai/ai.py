from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
import threading
import keyboard
import subprocess
import webbrowser
import spacy
import datetime
import pytz
import wikipedia
import requests
import json
import re
import openai


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    # Process the user input here
    return 'Success'  # Return the response as needed

if __name__ == '__main__':
    app.run(debug=True)
