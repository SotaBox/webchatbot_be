from config.connection import cursor , db_connection ,check_connection, DatabaseConnectionError
import mysql.connector

def get_user_by_username(username):
    try:
        check_connection()
        cursor.execute("SELECT * FROM user_table WHERE username = %s", (username,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def get_user_by_id(user_id):
    try:
        check_connection()
        cursor.execute("SELECT * FROM user_table WHERE id = %s", (user_id,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def insert_user(username, password, email, role='user'):
    try:
        check_connection()
        cursor.execute("INSERT INTO user_table (username, password, email, role) VALUES (%s, %s, %s, %s)", 
                       (username, password, email, role))
        db_connection.commit()
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def check_access_token(access_token):
    try:
        cursor.execute("SELECT id FROM user_table WHERE access_token = %s", (access_token,))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def check_refresh_token(refresh_token):
    try:
        cursor.execute("SELECT id FROM user_table WHERE refresh_token = %s", (refresh_token,))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def get_user_id_by_refresh_token(refresh_token):
    try:
        cursor.execute("SELECT id FROM user_table WHERE refresh_token = %s", (refresh_token,))
        result = cursor.fetchone()
        if result:
            return result['id']
        return None  

    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database error: {str(e)}")



def update_tokens(user_id, access_token, refresh_token):
    try:
        check_connection()
        cursor.execute("UPDATE user_table SET access_token = %s, refresh_token = %s WHERE id = %s", 
                       (access_token, refresh_token, user_id))
        db_connection.commit()
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def invalidate_tokens(user_id):
    try:
        check_connection()
        cursor.execute("UPDATE user_table SET access_token = NULL, refresh_token = NULL WHERE id = %s", (user_id,))
        db_connection.commit()
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")
