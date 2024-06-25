from flask import Blueprint
from flask_jwt_extended import jwt_required

# Import authentication functions
from handlers.auth_handlers.login import login_handler
from handlers.auth_handlers.register import register_handler
from handlers.auth_handlers.refresh_token import refresh_token_handler
from handlers.auth_handlers.logout import logout_handler
from handlers.auth_handlers.get_profile import get_profile_handler

routers_auth = Blueprint('auth', __name__)

@routers_auth.route('/auth/login', methods=['POST'])
def login():
    return login_handler()

@routers_auth.route('/auth/register', methods=['POST'])
def register():
    return register_handler()

@routers_auth.route('/auth/refresh-token', methods=['POST'])
def refresh_token():
    return refresh_token_handler()

@routers_auth.route('/auth/logout', methods=['GET'])
@jwt_required()
def logout():
    return logout_handler()

@routers_auth.route('/auth/get-profile', methods=['GET'])
@jwt_required()
def get_profile():
    return get_profile_handler()
