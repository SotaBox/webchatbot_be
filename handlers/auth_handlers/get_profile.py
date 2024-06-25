# get_profile.py
from flask import jsonify
from services.auth_services import AuthService

def get_profile_handler():
    response, status_code = AuthService.get_profile()
    return jsonify(response), status_code
