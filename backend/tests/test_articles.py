import json

# Test creating an article (this requires an authenticated user with 'editor' or 'admin' role)
def test_create_article(client):
    """
    Test case for creating an article by a logged-in user with 'editor' or 'admin' role.

    Steps:
    1. Register a user with 'editor' role and log in to get a JWT token.
    2. Use the token to create a new article.

    Asserts:
    - Status code should be 201 (Created), indicating the article was successfully created.
    - Response should confirm that the article was created.
    """
    # Register and log in to get a JWT token
    client.post('/auth/register', json={
        "email": "editor@example.com",
        "password": "editorpassword"
    })
    login_response = client.post('/auth/login', json={
        "email": "editor@example.com",
        "password": "editorpassword"
    })
    token = json.loads(login_response.data)["access_token"]

    # Create an article
    response = client.post('/articles', json={
        "title": "Test Article",
        "content": "This is a test article."
    }, headers={"Authorization": f"Bearer {token}"})

    # Assert that the article was created successfully
    assert response.status_code == 201
    assert b'Article created successfully!' in response.data


# Test retrieving all articles (publicly accessible)
def test_get_articles(client):
    """
    Test case for retrieving all articles (publicly accessible).

    Steps:
    1. Fetch the list of all articles.

    Asserts:
    - Status code should be 200, indicating the request was successful.
    """
    response = client.get('/articles')

    # Assert that the request was successful
    assert response.status_code == 200


# Test updating an article (this requires the article's author or an admin)
def test_update_article(client):
    """
    Test case for updating an article by the article's author.

    Steps:
    1. Log in as the article's author to get a JWT token.
    2. Create a new article.
    3. Use the token to update the article.

    Asserts:
    - Status code should be 200, indicating the update was successful.
    - Response should confirm that the article was updated.
    """
    # Log in as the article's author
    login_response = client.post('/auth/login', json={
        "email": "editor@example.com",
        "password": "editorpassword"
    })
    token = json.loads(login_response.data)["access_token"]

    # Create an article to be updated
    create_response = client.post('/articles', json={
        "title": "Article to Update",
        "content": "Initial content"
    }, headers={"Authorization": f"Bearer {token}"})

    # Extract the created article's ID
    article_id = create_response.json['id']

    # Update the article
    update_response = client.put(f'/articles/{article_id}', json={
        "title": "Updated Title",
        "content": "Updated content"
    }, headers={"Authorization": f"Bearer {token}"})

    # Assert that the article was updated successfully
    assert update_response.status_code == 200
    assert b'Article updated successfully!' in update_response.data
