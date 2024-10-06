import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def app():
    """
    Fixture to create the Flask application with a test configuration.
    
    This fixture uses the app factory pattern to create a Flask app configured for testing. 
    The database tables are created before running the tests and dropped afterward to ensure a clean test environment.

    Yields:
        Flask app instance for testing.
    """
    # Create the Flask app with test configurations
    app = create_app()

    # Update the app configuration for testing
    app.config.update({
        'TESTING': True,  # Enable testing mode
        'SQLALCHEMY_DATABASE_URI': app.config['SQLALCHEMY_DATABASE_URI'],  # Use the database URL from the environment
        'JWT_SECRET_KEY': 'test_secret_key',  # Set a secret key for JWT in tests
        'SQLALCHEMY_TRACK_MODIFICATIONS': False  # Disable modification tracking to improve performance
    })

    # Create all database tables within the app context
    with app.app_context():
        db.create_all()

    # Provide the app instance for the test cases
    yield app

    # Teardown: Drop all tables after tests are completed
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """
    Fixture to provide a test client for making requests to the Flask application.
    
    The client can be used in test cases to simulate HTTP requests without running a live server.
    
    Args:
        app: The Flask app instance from the `app` fixture.
    
    Returns:
        Flask test client.
    """
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    """
    Fixture to provide a CLI runner for testing Flask command-line interface (CLI) commands.
    
    The runner allows tests to simulate running Flask CLI commands, useful for testing things like migrations.
    
    Args:
        app: The Flask app instance from the `app` fixture.
    
    Returns:
        Flask CLI test runner.
    """
    return app.test_cli_runner()
