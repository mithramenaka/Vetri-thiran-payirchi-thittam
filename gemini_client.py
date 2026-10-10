import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class GeminiService:
    """
    Central Gemini API service used by all EduGenie modules.
    """

    def __init__(self):
        self.api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        ).strip()

        self.client = None

        if (
            self.api_key
            and self.api_key != "YOUR_GEMINI_API_KEY_HERE"
        ):
            self.client = genai.Client(
                api_key=self.api_key
            )

    def is_configured(self) -> bool:
        """
        Check whether Gemini has been configured.
        """

        return self.client is not None

    def generate(
        self,
        prompt: str,
        temperature: float = 0.4,
        max_output_tokens: int = 4096,
    ) -> str:
        """
        Generate normal text using Gemini.
        """

        if not self.is_configured():
            raise RuntimeError(
                "Gemini API key is missing. "
                "Please add GEMINI_API_KEY to your .env file."
            )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                ),
            )

            text = getattr(
                response,
                "text",
                None
            )

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except Exception as exc:
            raise RuntimeError(
                f"Gemini API error: {exc}"
            ) from exc

    def generate_json(
        self,
        prompt: str,
        temperature: float = 0.3,
        max_output_tokens: int = 4096,
    ) -> str:
        """
        Generate JSON text using Gemini JSON response mode.
        """

        if not self.is_configured():
            raise RuntimeError(
                "Gemini API key is missing. "
                "Please add GEMINI_API_KEY to your .env file."
            )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                    response_mime_type="application/json",
                ),
            )

            text = getattr(
                response,
                "text",
                None
            )

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty JSON response."
                )

            return text.strip()

        except Exception as exc:
            raise RuntimeError(
                f"Gemini JSON API error: {exc}"
            ) from exc


gemini_service = GeminiService()