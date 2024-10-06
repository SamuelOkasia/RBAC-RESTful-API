import redis
from flask import current_app

def get_redis_client():
    """
    Initializes and returns a Redis client instance.

    The function uses the current Flask app's configuration to connect to Redis.
    It defaults to the 'redis' host and port 6379 if no custom configuration is provided.

    Returns:
        StrictRedis: A Redis client instance ready to interact with the Redis server.
    """
    return redis.StrictRedis(
        host=current_app.config.get('REDIS_HOST', 'redis'),  # Defaults to 'redis' if not configured
        port=current_app.config.get('REDIS_PORT', 6379),     # Defaults to port 6379
        decode_responses=True                                # Ensures the responses are returned as Python strings
    )
