import os
import time
from openai import OpenAI, RateLimitError, APIError
from dotenv import load_dotenv

load_dotenv()

_MAX_RETRIES = 3
_RETRY_DELAY = 2.0
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
        _client = OpenAI(api_key=api_key)
    return _client


def call_llm(prompt: str, model: str = "gpt-4.1-mini") -> str:
    client = _get_client()
    last_error: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            response = client.responses.create(model=model, input=prompt)
            return response.output_text
        except RateLimitError as e:
            last_error = e
            time.sleep(_RETRY_DELAY * (attempt + 1))
        except APIError as e:
            last_error = e
            if attempt < _MAX_RETRIES - 1:
                time.sleep(_RETRY_DELAY)
    raise RuntimeError(f"LLM call failed after {_MAX_RETRIES} attempts: {last_error}")
