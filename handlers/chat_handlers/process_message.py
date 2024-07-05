from flask import jsonify, request
from services.chat_sevices import ChatService

def process_message_handler():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400

    access_token_error = ChatService.check_valid_access_token()
    if access_token_error:
        return jsonify(access_token_error[0]), access_token_error[1]

    message = data['message']
    response, status_code = ChatService.process_message(message)
    return jsonify(response), status_code   