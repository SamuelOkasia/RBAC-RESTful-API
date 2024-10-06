from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash

class User(db.Model):
    """
    User model representing users in the system. This model stores information about
    users, including email, password (hashed), role, and whether the user is a Google
    user or not.
    """
    
    __tablename__ = 'users'  # Explicitly set table name to 'users'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    email = db.Column(db.String(120), unique=True, nullable=False)  # User email, must be unique
    password = db.Column(db.String(255), nullable=True)  # User password (nullable for Google users)
    is_google_user = db.Column(db.Boolean, default=False)  # Flag to check if user registered via Google
    role = db.Column(db.String(20), nullable=False, default='user')  # Role of the user (default to 'user')

    def set_password(self, password):
        """
        Hashes the password and stores it securely.
        
        Args:
            password (str): The plaintext password to be hashed.
        """
        self.password = generate_password_hash(password)

    def __repr__(self):
        """
        Returns a string representation of the user object, useful for debugging.
        """
        return f"<User {self.email}>"

class Article(db.Model):
    """
    Article model representing articles posted by users. This model stores information
    about the article title, content, and the user who authored it.
    """
    
    # Define columns
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each article
    title = db.Column(db.String(255), nullable=False)  # Title of the article
    content = db.Column(db.Text, nullable=False)  # Content of the article
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Link to the User who authored the article
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Update timestamp

    # Define relationship to the User model
    author = db.relationship('User', backref='articles')

    def __repr__(self):
        """
        Returns a string representation of the article object, useful for debugging.
        """
        return f"<Article {self.title}>"
