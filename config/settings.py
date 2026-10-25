import os
from dotenv import load_dotenv


def load_config():
    """Loads environment variables from the .env file."""
    load_dotenv()


class Settings:
    """Centralized configuration variables."""
    # Chunking Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # LLM Configuration
    MODEL_NAME = "gpt-4o-mini"
    TEMPERATURE = 0

    # Embedding Configuration
    EMBEDDING_MODEL = "text-embedding-3-small"  # or standard OpenAI default


settings = Settings()
