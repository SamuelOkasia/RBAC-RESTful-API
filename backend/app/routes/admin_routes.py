from flask import jsonify, request, Blueprint
from app import db
from app.models import User
from app.utils import role_required
from flask_jwt_extended import jwt_required

# Blueprint for admin-related routes
admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    """
    Route to list all users in the system.
    Accessible only by users with the 'admin' role.
    
    Returns:
        JSON response with a list of all users and their roles.
    """
    # Query all users from the database
    users = User.query.all()

    # Convert the list of user objects into a dictionary
    user_list = [{"email": user.email, "role": user.role} for user in users]

    # Return the user list with a 200 OK status
    return jsonify(user_list), 200


@admin_blueprint.route('/promote', methods=['POST'])
@jwt_required()
@role_required('admin')
def promote_user():
    """
    Route to promote a user to a higher role.
    Accessible only by users with the 'admin' role.
    
    Request Body (JSON):
        email (str): The email of the user to promote.
        role (str): The new role to assign to the user.
    
    Returns:
        JSON response indicating success or failure.
    """
    # Get JSON data from the request body
    data = request.get_json()

    # Find the user by email
    user = User.query.filter_by(email=data['email']).first()

    # If the user is not found, return a 404 error
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update the user's role and commit the change to the database
    user.role = data['role']
    db.session.commit()

    # Return a success message with a 200 OK status
    return jsonify({"message": f"User {user.email} promoted to {user.role}!"}), 200
