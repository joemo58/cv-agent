from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def call_llm(prompt: str, model: str = "gpt-4.1-mini") -> str:
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text