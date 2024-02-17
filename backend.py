#!/usr/bin/python3

import mysql.connector as mysql
import os

# Load environment variables from .env file
env = {}
try:
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=")
                env[key] = value
except Exception as e:
    print("Failed to read environment variables from .env file:", e)
    exit(1)

# Database configuration
DB_HOST = env.get("DB_HOST", "localhost")
DB_USER = env.get("DB_USER", "root")
DB_PASSWORD = env.get("DB_PASSWORD", "")
DB_NAME = env.get("DB_NAME", "my_database")

# Connect to MySQL database
try:
    connection = mysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()
    print("Connected to MySQL database:", DB_NAME)
except mysql.Error as e:
    print("Failed to connect to MySQL:", e)
    exit(1)

# Define database operations
def create_table():
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                email VARCHAR(100)
            )
        """)
        connection.commit()
        print("Table 'users' created successfully.")
    except mysql.Error as e:
        print("Error creating table:", e)

def insert_user(username, email):
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        connection.commit()
        print("User inserted successfully.")
    except mysql.Error as e:
        print("Error inserting user:", e)

def fetch_users():
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Users:")
        for user in users:
            print(user)
    except mysql.Error as e:
        print("Error fetching users:", e)

# Main function
def main():
    create_table()
    insert_user("john_doe", "john@example.com")
    insert_user("jane_doe", "jane@example.com")
    fetch_users()

if __name__ == "__main__":
    main()
