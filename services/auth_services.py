# service.py
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from repo.user import get_user_by_username, invalidate_tokens, update_tokens,insert_user,check_access_token,get_user_by_id,check_refresh_token,get_user_id_by_refresh_token
from config.connection import DatabaseConnectionError
from flask import request
import re 
class AuthService:
    @staticmethod
    def login(username, password):
        try:
            user = get_user_by_username(username)
            if not user:
                return {'error': 'User not found'}, 404
            
            if user['password'] != password:
                return {'error': 'Invalid password'}, 401

            user_id = user['id']
            email = user['email']

            access_token = create_access_token(identity={"user_id": user_id, "username": username, "email": email})
            refresh_token = create_refresh_token(identity={"user_id": user_id})

            invalidate_tokens(user_id)
            update_tokens(user_id, access_token, refresh_token)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
            
        except DatabaseConnectionError as e:
            return {'error': 'Database connection error', 'details': str(e)}, 500
    
    @staticmethod
    def is_password_valid(password):
        if len(password) < 8 or len(password) > 32:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[\W_]", password):
            return False
        return True

    @staticmethod
    def is_email_valid(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    @staticmethod
    def register(username, password, email):
        if not username or not password or not email:
            return {'error': 'Username, password, and email are required'}, 400

        if not AuthService.is_password_valid(password):
            return {'error': 'Password must be 8-32 characters long and include uppercase, lowercase, digit, and special character'}, 400

        if not AuthService.is_email_valid(email):
            return {'error': 'Invalid email format'}, 400

        try:
            user = get_user_by_username(username)
            if user:
                return {'error': 'Username already exists'}, 409

            insert_user(username, password, email)

        except DatabaseConnectionError as e:
            return {'error': 'Database connection error', 'details': str(e)}, 500
        except Exception as e:
            return {'error': 'Failed to register user', 'details': str(e)}, 500

        return {'message': 'User registered successfully'}, 201
    
    @staticmethod
    def logout():
        try:
            current_user = get_jwt_identity()
            user_id = current_user["user_id"]
            
            invalidate_tokens(user_id)
            
            return {'message': 'User logged out successfully'}, 200
        except DatabaseConnectionError as e:
            return {'error': 'Database connection error', 'details': str(e)}, 500
        except Exception as e:
            return {'error': 'Failed to logout user', 'details': str(e)}, 500
        
    @staticmethod
    def get_profile():
        try:
            # Verify JWT in the request
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            
            if not current_user:
                return {'error': 'Missing JWT in request'}, 401
            
            user_id = current_user["user_id"]
            access_token = request.headers.get('Authorization').split()[1]  # Extract access token from the Authorization header

            # Check if access_token is valid
            if not check_access_token(access_token):
                return {'error': 'Invalid or expired access token'}, 401
            
            # Fetch user profile from database
            user = get_user_by_id(user_id)

            if user:
                profile = {
                    'user_id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
                return profile, 200
            else:
                return {'error': 'User not found'}, 404
        except DatabaseConnectionError as e:
            return {'error': 'Database connection error', 'details': str(e)}, 500
        except Exception as e:
            return {'error': 'Failed to fetch user profile', 'details': str(e)}, 500

    @staticmethod
    def refresh_token(refresh_token):
        try:
             # Check if refresh token exists in the database
            if not check_refresh_token(refresh_token):
                return {'error': 'Invalid or expired refresh token'}, 401
            # Verify the refresh token and get the user_id
            user_id = get_user_id_by_refresh_token(refresh_token)
            if not user_id:
                return {'error': 'Invalid or expired refresh token'}, 401

            # Fetch user details from the database
            user = get_user_by_id(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            # Generate new tokens
            access_token = create_access_token(identity={"user_id": user_id, "username": user["username"], "email": user["email"]})
            new_refresh_token = create_refresh_token(identity={"user_id": user_id})

            # Invalidate old tokens
            invalidate_tokens(user_id)

            # Save new tokens to the database
            update_tokens(user_id, access_token, new_refresh_token)

            return {
                'access_token': access_token,
                'refresh_token': new_refresh_token
            }, 200

        except DatabaseConnectionError as e:
            return {'error': 'Database connection error', 'details': str(e)}, 500
        except Exception as e:
            return {'error': 'An error occurred', 'details': str(e)}, 500

