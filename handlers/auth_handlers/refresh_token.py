# refresh_token.py
from flask import jsonify ,request
from services.auth_services import AuthService

def refresh_token_handler():
    data = request.get_json()
    if not data or 'refresh_token' not in data:
        return jsonify({'error': 'Refresh_token is required'}), 400

    refresh_token = data["refresh_token"]
    response, status_code = AuthService.refresh_token(refresh_token)
    return jsonify(response), status_code

