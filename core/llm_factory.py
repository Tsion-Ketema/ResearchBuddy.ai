from langchain_openai import ChatOpenAI
from config.settings import settings


def get_chat_model():
    """Instantiates and returns the configured LLM."""
    return ChatOpenAI(
        model_name=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE
    )
