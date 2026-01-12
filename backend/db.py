# backend/db.py
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Read DB configuration from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    """Establishes and returns a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            print("✅ Connected to MySQL database")
        return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    """Closes the given database connection."""
    if connection and connection.is_connected():
        connection.close()
        print("✅ MySQL connection closed")
