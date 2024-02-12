# !/usr/bin/python
'''JUPI-LEARN backend code - goutham santhosh'''
import mysql.connector as mys
import os
import re
import hashlib

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
	print("Failed to locate env file")
	os._exit(0)

#Global variables and configuation(from env file)
MYSQL_HOST = env["MYSQL_HOST"] #This can be the IP address of mysql running in google cloud(eg: 210.78.43.21)
MYSQL_USER = env["MYSQL_USER"]
MYSQL_PASSWORD = env["MYSQL_PASSWORD"]
MYSQL_DB = env["MYSQL_DB"]

#Functions that handle requests
def validate_signup(data):
	'''Validates signup information provided by the user'''
	errors = ""
	#Name
	if not str(data["name"]).replace(" ","SEPchar").isalpha():
		errors += "Name should only contain alphabets!. "
	#Email
	emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
	if not re.fullmatch(emailRegex,data["email"]):
		errors += "Invalid email!. "
	#Password
	password = hashlib.sha256(str(data["password"]).encode("UTF-8"))
	'''goutham --> Call create account here'''

	if errors == "":
		return (True,errors)
	else:
		return (False,errors)

#DB functions
def mysqlDB_init():
	'''Create mysql db if it doesn't exist'''
	dbExists = False
	con = mys.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD)
	cur = con.cursor()
	cur.execute("show databases;")
	for db in cur:
		if db[0] == MYSQL_DB:
			dbExists = True
			break
	if not dbExists:
		print("Creating database {} ...".format(MYSQL_DB))
		cur.execute("create database {};".format(MYSQL_DB))
	con.close()

def tableExists(table):
	'''Checks whether the table already exists'''
	tableExists = False
	con = mys.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD,database=MYSQL_DB)
	cur = con.cursor()
	cur.execute("show tables;")
	for t in cur:
		if t == table:
			tableExists = True
			break
	con.close()
	if tableExists:
		return True
	else:
		return False


'''#<Main code starts here>
#Connect to mysql server
mysqlDB_init()

try:
	con = mys.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD,database=MYSQL_DB)
	if con.is_connected():
		print("MySQL connection established...")
except Exception as e:
	error(e,"MySQL Connection error")

cur = con.cursor()

#Creating users table
#The table user has these fields by default(You may add/remove/modify fields or properties)
#	User ID - auto incrementing value
#	Username - 20 characters
#	Passwod - stored as hash using password() func
#	For saving password use sha2('password',512)
#	Name of user - 30 characters
#	Email - 20 characters
#More information such as age,gender etc cn be added
if not tableExists("users"):
	print("Creating table users...")
	cur.execute("create table users(user_id int primary key auto_increment ,username varchar(20),password char(128),name varchar(30),email varchar(20));")'''