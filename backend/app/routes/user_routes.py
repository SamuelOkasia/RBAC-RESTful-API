from flask import jsonify, request, Blueprint
from app import db
from app.models import User
from flask_jwt_extended import jwt_required
import redis
import json

# Define Blueprint for user-related routes
user_blueprint = Blueprint('user', __name__)

# Initialize Redis connection (assumes Redis is running on the same network)
r = redis.from_url('redis://redis:6379')

@user_blueprint.route('/profile/<email>', methods=['GET'])
@jwt_required()
def get_profile(email):
    """
    Retrieves the profile of a user by their email.
    
    This route first checks if the user's profile is cached in Redis. If cached, the profile is returned directly
    from Redis. If not, it queries the database to fetch the user's profile, caches it in Redis, and returns the data.

    Args:
        email (str): The email of the user whose profile is being retrieved.
    
    Returns:
        JSON: The user's profile information (email and role).
        404: If the user does not exist.
    """
    # Check if the profile is cached in Redis
    cached_profile = r.get(f"profile:{email}")
    if cached_profile:
        # Return cached profile if found
        return jsonify(json.loads(cached_profile)), 200

    # Query the database for the user's profile
    user = User.query.filter_by(email=email).first()

    # If user is not found, return a 404 error
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Cache the user's profile in Redis (expires in 1 hour)
    profile_data = {"email": user.email, "role": user.role}
    r.set(f"profile:{email}", json.dumps(profile_data), ex=3600)

    # Return the user's profile
    return jsonify(profile_data), 200
