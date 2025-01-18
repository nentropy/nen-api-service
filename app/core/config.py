import os

from dotenv import load_dotenv

# Load environment variables from `.env` file
load_dotenv()

class Config:
    # Redis Configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

    # Portkey Configuration
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")

    # LangSmith Configuration
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    
    # RABBITMQ
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

    # Debug Mode
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

config = Config()
