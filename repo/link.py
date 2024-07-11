import mysql.connector
from config.connection import cursor, db_connection, check_connection, DatabaseConnectionError

def check_link_exists(link):
    try:
        check_connection()
        query = "SELECT COUNT(*) as count FROM link WHERE link = %s"
        cursor.execute(query, (link,))
        result = cursor.fetchone()
        return result['count'] > 0
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def insert_link(link, parent_id):
    try:
        check_connection()
        query = "INSERT INTO link (link, parent_id) VALUES (%s, %s)"
        cursor.execute(query, (link, parent_id,))
        db_connection.commit()
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def insert_data_link(link, title, description, content, vector_status):
    try:
        check_connection()
        query = """
        UPDATE link
        SET title = %s, description = %s, content = %s, vector_status = %s
        WHERE link = %s
        """
        cursor.execute(query, (title, description, content, vector_status, link,))
        db_connection.commit()
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")
    
def get_link_by_id(link_id):
    try:
        check_connection()
        query = "SELECT link FROM link WHERE id = %s"
        cursor.execute(query, (link_id,))
        result = cursor.fetchone()
        return result['link'] if result else None
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def get_list_link_by_parent_id(parent_id):
    try:
        check_connection()
        query = """
        SELECT l.id, l.link 
        FROM link l 
        INNER JOIN parent_link pl ON l.parent_id = pl.id 
        WHERE pl.id = %s
        """
        cursor.execute(query, (parent_id,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")
    
def get_data_link(link_id):
    try:
        check_connection()
        query = "SELECT id, link, title, description, vector_status FROM link WHERE id = %s"
        cursor.execute(query, (link_id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Database error: {str(e)}")