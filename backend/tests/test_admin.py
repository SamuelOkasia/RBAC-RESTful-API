import json

# Test promoting a user (requires admin privileges)
def test_promote_user(client):
    """
    Test case for promoting a user to a higher role (e.g., 'editor') using the admin role.

    Steps:
    1. Register an admin user and log in to get a JWT token.
    2. Register a regular user.
    3. Use the admin token to promote the regular user to 'editor' role.

    Asserts:
    - Status code should be 200, indicating the promotion was successful.
    - Response data should confirm the user has been promoted to 'editor'.
    """
    # First, register an admin user and log in
    client.post('/auth/register', json={
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    login_response = client.post('/auth/login', json={
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    admin_token = json.loads(login_response.data)["access_token"]

    # Register a regular user
    client.post('/auth/register', json={
        "email": "user@example.com",
        "password": "userpassword"
    })

    # Promote the regular user to 'editor' role
    promote_response = client.post('/admin/promote', json={
        "email": "user@example.com",
        "role": "editor"
    }, headers={"Authorization": f"Bearer {admin_token}"})

    # Assert that the promotion was successful
    assert promote_response.status_code == 200
    assert b'User user@example.com promoted to editor!' in promote_response.data

# Test listing all users (requires admin privileges)
def test_list_users(client):
    """
    Test case for listing all users in the system, accessible only by admins.

    Steps:
    1. Log in as an admin to get a JWT token.
    2. Use the token to request a list of users from the system.

    Asserts:
    - Status code should be 200, indicating the request was successful.
    - The response should contain both the admin's and the regular user's emails.
    """
    # Log in as admin to get the JWT token
    login_response = client.post('/auth/login', json={
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    admin_token = json.loads(login_response.data)["access_token"]

    # Request the list of users
    response = client.get('/admin/users', headers={"Authorization": f"Bearer {admin_token}"})

    # Assert that the request was successful and contains the expected users
    assert response.status_code == 200
    assert b'admin@example.com' in response.data
    assert b'user@example.com' in response.data
