import mysql.connector
from config.connection import cursor, db_connection, check_connection, DatabaseConnectionError

def insert_link_to_db(link, crawled_at):
    try:
        check_connection()
        cursor.execute("INSERT INTO url_sitemap (url, crawled_at) VALUES (%s, %s)", (link, crawled_at))
        db_connection.commit()
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def check_link_exists(link):
    try:
        check_connection()
        cursor.execute("SELECT 1 FROM url_sitemap WHERE url = %s LIMIT 1", (link,))
        result = cursor.fetchone() 
        return result is not None
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def insert_data_to_db(link, title, description, content, vector_status):
    try:    
        check_connection()
        cursor.execute("UPDATE url_sitemap SET title=%s, description=%s, content=%s, vector_status=%s WHERE url=%s",(title, description, content, vector_status, link))
        db_connection.commit()
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def get_list_link_from_db(url):
    try:
        check_connection()
        cursor.execute("SELECT id, url FROM url_sitemap WHERE crawled_at = %s", (url,))
        result = cursor.fetchall()  
        return result
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def get_data_link(link):
    try:
        check_connection()
        cursor.execute("SELECT id, title, description, vector_status FROM url_sitemap WHERE url = %s", (link,))
        result = cursor.fetchone()  
        return result
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")

def get_data_url(url):
    try:
        check_connection()
        cursor.execute("SELECT id, url, title, description, vector_status FROM url_sitemap WHERE crawled_at = %s", (url,))
        result = cursor.fetchall()  
        return result
    except mysql.connector.Error as e:
        db_connection.rollback()
        raise DatabaseConnectionError(f"Database error: {str(e)}")
