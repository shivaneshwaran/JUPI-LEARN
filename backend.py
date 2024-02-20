# JUPI-LEARN Backend - Created by [ S SHIVANESHWARAN ]

import mysql.connector as mys
import os
import re
import hashlib
import random
import smtplib
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Global variables
load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
SECRET_KEY = os.getenv("SECRET_KEY")
MAIL_ID = os.getenv("MAIL_ID")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

# Function to initialize MySQL database
def mysqlDB_init():
    dbExists = False
    try:
        con = mys.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)
        cur = con.cursor()
        cur.execute("show databases;")
        for db in cur:
            if db[0] == MYSQL_DB:
                dbExists = True
                break
        if not dbExists:
            cur.execute("create database {};".format(MYSQL_DB))
        con.close()
    except:
        print("MySQL connection failed!")
        os._exit(0)

# Main code starts here
# Initialize encryption
fernet = Fernet(SECRET_KEY)

# Generate salt for hashing password
def gen_salt(length):
    charSet = "abcdefghijklmnopqrstuvwxyz1234567890"
    salt = ""
    for i in range(length):
        r1 = random.randint(0, len(charSet) - 1)
        c = charSet[r1]
        if c.isalpha():
            r2 = random.randint(0, 1)
            if r2 == 0:
                salt += c
            else:
                salt += c.upper()
        else:
            salt += c
    return salt

# Connect to MySQL server and create users table if not exists
mysqlDB_init()

try:
    con = mys.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
    if con.is_connected():
        print("MySQL connection established...")
except Exception as e:
    print("MySQL Connection error")

cur = con.cursor()

try:
    cur.execute("create table users(user_id int primary key auto_increment, name varchar(256), email varchar(320), password char(64), salt char(32), prompt varchar(3000));")
except:
    pass

# Function to retrieve data from users table
def db():
    db = []
    cur.execute("SELECT * FROM users;")
    for i in cur:
        db.append(i)
    return db

# Function to send welcome mail to new users
def send_mail(address, name):
    try:
        mailServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        mailServer.ehlo()
        mailServer.login(MAIL_ID, MAIL_PASSWORD)
    except:
        print("Failed connecting to Gmail server")
    try:
        mSubject = "Welcome to JUPI-Learning"
        mBody = f"Hello {name},\n\nWelcome to JUPI Learning! Your account has been created with username as your email address.\n\nSign in to start your journey: https://jupilearning.app"
        mText = f"From: {MAIL_ID}\nSubject: {mSubject}\n\n{mBody}"
        mailServer.sendmail(MAIL_ID, [address], mText)
        mailServer.close()
    except:
        print(f"Failed to send message to {address}")

# Function to create a new user account
def create_account(name, email, password):
    accountExists = False
    for i in db():
        e = i[2]
        if e == email:
            accountExists = True
            break
    if not accountExists:
        salt = gen_salt(32)
        p = hashlib.sha256(str(password + salt).encode("UTF-8")).hexdigest()
        cur.execute(f"insert into users (name, email, password, salt, prompt) values ('{name}', '{email.lower()}', '{p}', '{salt}', '')")
        con.commit()
        send_mail(email.lower(), name)
        return True
    else:
        return False

# Function to authenticate user sign in
def signin_account(data):
    email = data["email"].lower()
    password = data["password"]
    matches = False
    sessionID = ""
    for i in db():
        e, p, s = i[2], i[3], i[4]
        pHash = hashlib.sha256(str(password + s).encode("UTF-8")).hexdigest()
        if e == email and p == pHash:
            matches = True
            sessionID = fernet.encrypt(f"{email}<{pHash}".encode()).decode()
            break
    return (matches, sessionID)

# Function to validate user token
def validate_token(token):
    validated = False
    username = ""
    try:
        email, password = fernet.decrypt(token.encode()).decode().split("<>")
        for i in db():
            u, e, p = i[1], i[2], i[3]
            if e == email and p == password:
                validated = True
                username = u
                break
        return (validated, username)
    except:
        return (False, username)

# Function to validate user signup data
def validate_signup(data):
    errors = ""
    if not str(data["name"]).replace(" ", "SEP").isalpha():
        errors += "Name should only contain alphabets!. "
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(emailRegex, data["email"]):
        errors += "Invalid email!. "
    if len(data["name"]) > 256:
        errors += "Name should only have 256 characters!. "
    if len(data["email"]) > 320:
        errors += "Email should only have 320 characters!. "
    if errors == "":
        acCreated = create_account(data["name"], data["email"], data["password"])
        if not acCreated:
            errors += "Account already exists!. "
            return (False, errors)
        return (True, errors)
    else:
        return (False, errors)

# End of Backend Code
