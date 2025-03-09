import anthropic

from .claud_config import CLAUD_API_KEY


CLAUD_CLIENT = anthropic.Anthropic(
    api_key=CLAUD_API_KEY,
)
