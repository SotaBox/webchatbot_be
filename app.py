from config.config import Config
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

# Import the blueprint
from routers.auth_routers import routers_auth
from routers.chat_routers import routers_chat
from routers.crawl_routers import routers_crawl

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' :  "ChatBot_API"
    }
)

# Configure app
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.JWT_REFRESH_TOKEN_EXPIRES

# Initialize JWTManager
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(swaggerui_blueprint,url_prefix = SWAGGER_URL)
app.register_blueprint(routers_auth)
app.register_blueprint(routers_chat)
app.register_blueprint(routers_crawl)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
