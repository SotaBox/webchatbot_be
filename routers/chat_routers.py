from flask import Blueprint
from flask_jwt_extended import jwt_required

# Import authentication functions
from handlers.chat_handlers.process_message import process_message_handler
from handlers.chat_handlers.get_url import get_list_url_handler

routers_chat = Blueprint('chat', __name__)

@routers_chat.route('/chat/process-message', methods=['POST'])
@jwt_required()
def prrocess_message():
    return process_message_handler()

@routers_chat.route('/chat/get_list_url', methods = ['GET'])
@jwt_required()
def get_url():
    return get_list_url_handler()