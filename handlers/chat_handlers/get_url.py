from flask import jsonify, request
from services.chat_sevices import ChatService

def get_list_url_handler():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    access_token_error = ChatService.check_valid_access_token()
    if access_token_error:
        return jsonify(access_token_error[0]), access_token_error[1]

    response, status_code = ChatService.get_url_data(url)
    return jsonify(response), status_code
