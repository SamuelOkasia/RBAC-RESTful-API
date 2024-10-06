from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User
from app.redis_client import get_redis_client

def rate_limit(max_attempts, window_seconds):
    """
    A decorator to enforce rate limiting based on the number of allowed requests in a time window.
    
    Args:
        max_attempts (int): Maximum number of requests allowed.
        window_seconds (int): Time window in seconds for the rate limit.
        
    Returns:
        Function: The decorated function that applies rate limiting.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Get the client's IP address to use as the rate limit key
            ip = request.remote_addr
            key = f"rate_limit:{ip}"
            redis_client = get_redis_client()  # Initialize Redis client

            # Check the number of current attempts made by the IP
            current_attempts = redis_client.get(key)

            # If attempts exceed the limit, return a 429 Too Many Requests error
            if current_attempts and int(current_attempts) >= max_attempts:
                return jsonify({"error": "Too many requests"}), 429

            # Increment the number of attempts and set an expiration for the time window
            redis_client.incr(key)
            redis_client.expire(key, window_seconds)
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

def role_required(role):
    """
    A decorator to enforce role-based access control (RBAC) on routes.

    Args:
        role (str): The role required to access the decorated route.

    Returns:
        Function: The decorated function that applies role-based access control.
    """
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()  # Ensure the route requires a valid JWT token
        def decorated_view(*args, **kwargs):
            # Get the current user's email from the JWT token
            current_user_email = get_jwt_identity()
            user = User.query.filter_by(email=current_user_email).first()

            # If the user doesn't exist or their role doesn't match, return a 403 Forbidden error
            if not user or user.role != role:
                return jsonify({"error": "Access forbidden: Insufficient permissions"}), 403

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
