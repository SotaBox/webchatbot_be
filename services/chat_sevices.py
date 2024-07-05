from config.connection import DatabaseConnectionError
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import request
import requests
from repo.user import check_access_token
from repo.url import get_list_url_from_db
from config.config import Config
from package.http.http import HttpClient
import logging

class ChatService:
    @staticmethod
    def check_valid_access_token():
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()

            if not current_user:
                return {'error': 'Missing JWT in request'}, 401
            
            access_token = request.headers.get('Authorization').split()[1] 

            # Check if access_token is valid
            if not check_access_token(access_token):
                return {'error': 'Invalid or expired access token'}, 401

            return None 

        except Exception as e:
            logging.error("Error checking access token: %s", str(e))
            return {'error': str(e)}, 500
    
    @staticmethod
    def process_message(message):
        try:
            # Call Azure OpenAI API to get response
            response_message = ChatService.call_azure_openai_api(message)

            return {
                "message-bot": response_message
            }, 200

        except DatabaseConnectionError as e:
            logging.error("Database connection error: %s", str(e))
            return {'error': 'Database connection error', 'details': str(e)}, 500
        except Exception as e:
            logging.error("Error processing message: %s", str(e))
            return {'error': 'An error occurred while processing the message', 'details': str(e)}, 500
        
    @staticmethod
    def call_azure_openai_api(message, max_tokens=None):
        try:
            if max_tokens is None:
                max_tokens = int(Config.AZURE_GPT_35_MAX_TOKEN)

            api_url, payload, headers = HttpClient.post_to_azure_open_ai(message)

            response = requests.post(api_url, json=payload, headers=headers)
 
            if response.status_code == 200:
                result = response.json()

                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content'].strip()
                else:
                    logging.error("Azure OpenAI API returned an unexpected response format: %s", result)
                    return "Sorry, I couldn't process that request at the moment."
            else:
                logging.error("Azure OpenAI API error: %s", response.text)
                return "Sorry, I couldn't process that request at the moment."

        except Exception as e:
            logging.error("Error calling Azure OpenAI API: %s", str(e))
            return "Sorry, I couldn't process that request at the moment."
    
    @staticmethod 
    def get_url_data(url):
        try:
            data= get_list_url_from_db(url)
            if data:
                return data, 200
            else:
                return {'error': 'Data not found for the given URL'}, 404
        except Exception as e:
            logging.error("Error getting URL data: %s", str(e))
            return {'error': 'An error occurred while getting URL data', 'details': str(e)}, 500