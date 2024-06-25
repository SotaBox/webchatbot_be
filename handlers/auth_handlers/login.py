#login.py
from flask import jsonify, request
from services.auth_services import AuthService

def login_handler():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']

    response, status_code = AuthService.login(username, password)
    return jsonify(response), status_code
