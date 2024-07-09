from flask import Blueprint
from flask_jwt_extended import jwt_required

# Import authentication functions
from handlers.chat_handlers.process_message import process_message_handler

routers_chat = Blueprint('chat', __name__)

@routers_chat.route('/chat/process-message', methods=['POST'])
@jwt_required()
def prrocess_message():
    return process_message_handler()

