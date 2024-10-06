from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_session import Session
import redis
import os

# Load environment variables from a .env file
load_dotenv()

# Initialize extensions without binding them to the app yet
db = SQLAlchemy()  # SQLAlchemy for database management
migrate = Migrate()  # Migrate for handling database migrations
oauth = OAuth()  # OAuth for handling external authentication
jwt = JWTManager()  # JWTManager for handling JWT-based authentication
sess = Session()  # Flask-Session for managing user sessions

def create_app():
    """
    Application factory function to create and configure a Flask app instance.

    This function initializes the app and sets up various extensions and blueprints.
    The app is configured using environment variables loaded via dotenv.
    
    Returns:
        app (Flask): The Flask app instance.
    """
    app = Flask(__name__)

    # Load configuration from 'config.Config' class
    app.config.from_object('config.Config')

    # Initialize extensions with the app
    db.init_app(app)  # Bind SQLAlchemy to the app
    migrate.init_app(app, db)  # Bind Migrate to the app and database
    oauth.init_app(app)  # Bind OAuth to the app
    jwt.init_app(app)  # Bind JWTManager to the app
    sess.init_app(app)  # Bind Session to the app



    # Register blueprints (modular sections of the app, each handling a specific part of the API)
    from app.routes.admin_routes import admin_blueprint
    from app.routes.article_routes import article_blueprint
    from app.routes.auth_routes import auth_blueprint
    from app.routes.user_routes import user_blueprint

    app.register_blueprint(admin_blueprint, url_prefix='/admin')  # Admin-related routes
    app.register_blueprint(article_blueprint, url_prefix='/articles')  # Article-related routes
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # Authentication-related routes
    app.register_blueprint(user_blueprint, url_prefix='/user')  # User-related routes

    return app
