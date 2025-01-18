import redis
from config import Config
import json
from logger import setup_logging

logger = setup_logging()

config = Config()

# Initialize Redis client
redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    decode_responses=True  # Automatically decode Redis responses as strings
)

def store_short_term_memory(key: str, data: dict, ttl: int = 86400):
    """
    Store data in Redis with an expiration time (default 24 hours).
    """
    try:
        redis_client.setex(key, ttl, json.dumps(data))
        logger.info(f"Data stored in Redis with key: {key} and TTL: {ttl}")
    except Exception as e:
        logger.error(f"Error storing data in Redis: {e}")

def get_short_term_memory(key: str):
    """
    Retrieve data from Redis by key.
    """
    try:
        data = redis_client.get(key)
        if data:
            logger.info(f"Data retrieved from Redis with key: {key}")
        else:
            logger.warning(f"No data found in Redis for key: {key}")
        return data
    except Exception as e:
        logger.error(f"Error retrieving data from Redis: {e}")
        return None
