import mysql.connector
from config.config import Config

db_connection = mysql.connector.connect(
    host=Config.DB_HOST,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME
)

cursor = db_connection.cursor(dictionary=True)

class DatabaseConnectionError(Exception):
    pass

def check_connection():
    try:
        db_connection.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database connection error: {str(e)}")
