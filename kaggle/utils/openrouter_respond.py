# THis is for local testing only.
import os
from typing import Literal, List, Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class ChatClient:
    def __init__(self, temperature: float = 1.0,
                 seed: int = 42,
                 model: str = "qwen/qwen3-8b"):
        """Initialize the chat client with OpenRouter configuration."""
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in .env file or environment variables")
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
        self.model = model
        self.temperature = temperature
        self.seed = seed

    def create_completion(self, messages: List[Dict[str, Any]]):
        """Create a chat completion with optional tool support."""
        extra_body = {
            "include_reasoning": True,
            "seed": self.seed,
        }

        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            extra_body=extra_body
        )

    def respond(self, prompt: str, system: str = ''):
        messages = [{"role": "user", "content": prompt}]
        if system:
            messages =  [{"role": "system", "content": system}] + messages
        return self.create_completion(messages).choices[0].message.content