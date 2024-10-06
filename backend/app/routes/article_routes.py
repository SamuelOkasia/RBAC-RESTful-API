import json
from flask import jsonify, request, Blueprint
from app import db
from app.models import Article, User
from app.utils import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.redis_client import get_redis_client

# Blueprint for article-related routes
article_blueprint = Blueprint('article', __name__)

# Helper function to convert datetime objects to string
def serialize_datetime(dt):
    """
    Convert datetime objects to ISO 8601 formatted string.
    
    Args:
        dt (datetime): A datetime object.
    
    Returns:
        str: ISO 8601 formatted string.
    """
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt

# Create an article (only accessible by users with 'editor' or 'admin' roles)
@article_blueprint.route('/', methods=['POST'])
@jwt_required()
@role_required('editor')  # Only editors can create articles
def create_article():
    """
    Create a new article.
    Only accessible by users with 'editor' or 'admin' roles.
    
    Request Body (JSON):
        - title (str): The title of the article.
        - content (str): The content of the article.
    
    Returns:
        JSON response with success message or error message.
    """
    data = request.get_json()
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    # Check if both title and content are provided
    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400

    # Create a new article
    article = Article(title=data['title'], content=data['content'], author=user)
    db.session.add(article)
    db.session.commit()

    # Clear the articles cache when a new article is added
    redis_client = get_redis_client
    redis_client.delete('articles')

    return jsonify({'message': 'Article created successfully!'}), 201

# Get all articles (publicly accessible) with Redis caching
@article_blueprint.route('/', methods=['GET'])
def get_articles():
    """
    Retrieve all articles. 
    Articles are cached in Redis to improve performance.
    
    Returns:
        JSON response with a list of all articles.
    """
    redis_client = get_redis_client

    # Check if articles are cached in Redis
    cached_articles = redis_client.get('articles')
    if cached_articles:
        return jsonify(json.loads(cached_articles)), 200

    # If not cached, fetch articles from the database
    articles = Article.query.all()
    result = [
        {"title": article.title, "content": article.content, "author": article.author.email, "created_at": serialize_datetime(article.created_at)}
        for article in articles
    ]

    # Cache the articles in Redis for 1 hour (3600 seconds)
    redis_client.set('articles', json.dumps(result), ex=3600)

    return jsonify(result), 200

# Get a single article by ID (publicly accessible) with Redis caching
@article_blueprint.route('/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """
    Retrieve a single article by its ID.
    Articles are cached in Redis to improve performance.
    
    Args:
        article_id (int): The ID of the article.
    
    Returns:
        JSON response with the article data.
    """
    redis_client = get_redis_client

    # Check if the article is cached in Redis
    cached_article = redis_client.get(f'article:{article_id}')
    if cached_article:
        return jsonify(json.loads(cached_article)), 200

    # If not cached, fetch article from the database
    article = Article.query.get_or_404(article_id)
    result = {
        "title": article.title,
        "content": article.content,
        "author": article.author.email,
        "created_at": serialize_datetime(article.created_at)
    }

    # Cache the article in Redis for 1 hour
    redis_client.set(f'article:{article_id}', json.dumps(result), ex=3600)

    return jsonify(result), 200

# Update an article (only accessible by the article's author or admins)
@article_blueprint.route('/<int:article_id>', methods=['PUT'])
@jwt_required()
def update_article(article_id):
    """
    Update an existing article by its ID.
    Only accessible by the article's author or users with 'admin' role.
    
    Args:
        article_id (int): The ID of the article to be updated.
    
    Request Body (JSON):
        - title (str): The new title of the article (optional).
        - content (str): The new content of the article (optional).
    
    Returns:
        JSON response with success or error message.
    """
    data = request.get_json()
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    # Fetch the article to be updated
   
