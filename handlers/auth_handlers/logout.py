# logout.py
from flask import jsonify
from services.auth_services import AuthService

def logout_handler():
    response, status_code = AuthService.logout()
    return jsonify(response), status_code
