import mysql.connector
from config.connection import cursor, db_connection, check_connection, DatabaseConnectionError

def check_parent_link_exists(parent_link):
    try:
        check_connection()
        query = "SELECT COUNT(*) as count FROM parent_link WHERE parent_link = %s"
        cursor.execute(query, (parent_link,))
        result = cursor.fetchone()
        return result['count'] > 0
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def insert_parent_link(parent_link):
    try:
        check_connection()
        query = "INSERT INTO parent_link (parent_link) VALUES (%s)"
        cursor.execute(query, (parent_link,))
        db_connection.commit()
        return cursor.lastrowid  # Retrieve the last inserted ID
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def get_id_by_parent_link(parent_link):
    try:
        check_connection()
        query = "SELECT id FROM parent_link WHERE parent_link = %s"
        cursor.execute(query, (parent_link,))
        result = cursor.fetchone()
        return result['id'] if result else None
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def get_data_parent_link(parent_link):
    try:
        check_connection()
        query = """
        SELECT l.id, l.link, l.title, l.description, l.vector_status 
        FROM link l 
        INNER JOIN parent_link pl ON pl.id = l.parent_id 
        WHERE pl.parent_link = %s
        """
        cursor.execute(query, (parent_link,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")
