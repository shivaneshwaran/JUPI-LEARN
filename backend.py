# !/usr/bin/python
'''JUPI-LEARN backend code - goutham santhosh'''
import mysql.connector 
import os
import re
import hashlib
import random
from cryptography.fernet import Fernet

env = {}
try:
	with open(".env") as f:
		while True:
			x = f.readline()
			if x:
				x = x.strip()
				if not x.startswith("#"):
					key,value = x.split("=")
					env[key] = value
			else:
				break
except:
	print("Failed to read env file")
	os._exit(0)


#Global variables and configuation(from env file)
MYSQL_HOST = env["MYSQL_HOST"] #This can be the IP address of mysql running in google cloud(eg: 210.78.43.21)
MYSQL_USER = env["MYSQL_USER"]
MYSQL_PASSWORD = env["MYSQL_PASSWORD"]
MYSQL_DB = env["MYSQL_DB"]
SECRET_KEY = (env["SECRET_KEY"] + "=").encode()

def mysqlDB_init():
	'''Create mysql db if it doesn't exist'''
	dbExists = False
	try:
		con = mys.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD)
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



#<Main code starts here>
#Initialize encryption
fernet = Fernet(SECRET_KEY)

def gen_salt(length):
	'''Generate salt for hashing password'''
	charSet = "abcdefghijklmnopqrstuvwxyz1234567890"
	salt = ""
	for i in range(length):
		r1 = random.randint(0,len(charSet)-1)
		c = charSet[r1]
		if c.isalpha():
			r2 = random.randint(0,1)
			if r2 == 0:
				salt += c
			else:
				salt += c.upper()
		else:
			salt += c
	return salt


#Connect to mysql server
mysqlDB_init()

try:
	con = mys.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD,database=MYSQL_DB)
	if con.is_connected():
		print("MySQL connection established...")
except Exception as e:
	print("MySQL Connection error")

cur = con.cursor()


#Creating users table
#The table user has these fields by default(You may add/remove/modify fields or properties)
#	User ID - auto incrementing value
#	Name of user - 256 characters
#	Email - 320 characters
#	Password - stored as hash(sha-256)
#	Salt - 32 char
#	Prompt - 3000 char limit(to store prompts from user)

try:
	cur.execute("create table users(user_id int primary key auto_increment, name varchar(256),email varchar(320), password char(64), salt char(32), prompt varchar(3000));")
except:
	pass

def db():
	db = []
	cur.execute("select * from users;")
	for i in cur:
		db.append(i)
	return db

def create_account(name,email,password):
	'''Create user account'''
	accountExists = False
	for i in db():
		e = i[2]
		if e == email:
			accountExists = True
			break
	if not accountExists:
		salt = gen_salt(32)
		p = hashlib.sha256(str(password + salt).encode("UTF-8")).hexdigest()
		cur.execute("insert into users (name,email,password,salt,prompt) values('{}','{}','{}','{}','')".format(name,email.lower(),p,salt))
		con.commit()
		return True
	else:
		return False

def signin_account(data):
	'''Check whether the provided credentials are correct and authenticate'''
	email = data["email"].lower()
	password = data["password"]
	matches = False
	sessionID = ""
	for i in db():
		e,p,s = i[2],i[3],i[4]
		pHash = hashlib.sha256(str(password + s).encode("UTF-8")).hexdigest()
		if e == email and p == pHash:
			matches = True
			sessionID = fernet.encrypt("{}<>{}".format(email,pHash).encode()).decode()
			break
	return (matches,sessionID)

def validate_token(token):
	'''Validate token in the client side'''
	validated = False
	username = ""
	try:
		email,password = fernet.decrypt(token.encode()).decode().split("<>")
		for i in db():
			u,e,p = i[1],i[2],i[3]
			if e == email and p == password:
				validated = True
				username = u
				break
		return (validated,username)
	except:
		return (False,username)


#Functions that handle requests
def validate_signup(data):
	'''Check and report errors in user supplied information'''
	'''Validates signup information provided by the user'''
	errors = ""
	#Name
	if not str(data["name"]).replace(" ","SEP").isalpha():
		errors += "Name should only contain alphabets!. "
	#Email
	emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
	if not re.fullmatch(emailRegex,data["email"]):
		errors += "Invalid email!. "

	#Checking length of data types
	if len(data["name"]) > 256:
		errors += "Name should only have 256 characters!. "
	if len(data["email"]) > 320:
		errors += "Email should only have 320 characters!. "

	if errors == "":
		acCreated = create_account(data["name"],data["email"],data["password"])
		if not acCreated:
			errors += "Account already exists!. "
			return (False,errors)
		return (True,errors)
	else:
		return (False,errors)
