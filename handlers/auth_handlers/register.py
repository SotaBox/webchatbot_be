# register.py
from flask import jsonify, request
from services.auth_services import AuthService

def register_handler():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    response, status_code = AuthService.register(username, password, email)
    return jsonify(response), status_code
