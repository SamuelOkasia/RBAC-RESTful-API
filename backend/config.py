import os
import redis

class Config:
    """
    Configuration class for loading environment variables and setting up app configurations.
    
    This class loads essential environment variables such as the JWT secret key, database connection
    string, Google OAuth credentials, and Redis settings. It also sets up configurations for session
    management, OAuth settings, and SQLAlchemy.
    """

    # Secret key for session management (required by Flask)
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Default value if not set

    # JWT (JSON Web Token) secret key for securing token-based authentication
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsupersecretkey')  # Default value if not set

    # SQLAlchemy database configuration, loaded from environment variables
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://flaskuser:flaskpassword@localhost:5432/flaskdb')

    # Google OAuth credentials, required for social login via Google
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

    # OAuth settings for development, these should be handled carefully in production
    OAUTHLIB_INSECURE_TRANSPORT = True  # Insecure transport allowed during development (HTTPS not required)
    OAUTHLIB_RELAX_TOKEN_SCOPE = True  # Allows more relaxed token scopes during OAuth flows

    # SQLAlchemy configuration to disable unnecessary modification tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis configuration for session management (used to store sessions in Redis)
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False  # Sessions are not permanent; they will expire
    SESSION_USE_SIGNER = True  # Sign session cookies to prevent tampering
    SESSION_REDIS = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'))  # Redis URL from environment

# Instantiating the configuration object (optional depending on how the app is configured)
config = Config()
