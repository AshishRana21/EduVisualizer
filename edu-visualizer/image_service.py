"""Image generation service using Hugging Face, Gemini, or OpenAI."""
import os
import requests
from io import BytesIO
from PIL import Image

from google import genai
from google.genai import types
from huggingface_hub import InferenceClient
from openai import OpenAI

IMAGE_SIZE = os.getenv("IMAGE_SIZE", "1024x1024")
IMAGE_QUALITY = os.getenv("IMAGE_QUALITY", "standard")

from provider_config import get_image_model, get_image_provider

STYLE_PREFIX = (
    "Educational illustration, clean infographic style, vibrant colors, "
    "white background, suitable for a student flashcard. Concept: "
)


def generate_image(prompt: str) -> Image.Image:
    """
    Generate an image from a text prompt and return a PIL Image.
    """
    full_prompt = STYLE_PREFIX + prompt
    provider = get_image_provider()
    image_model = get_image_model()

    if provider == "huggingface":
        width, height = _parse_size(IMAGE_SIZE)
        client = InferenceClient(api_key=os.getenv("HUGGINGFACE_API_KEY"))
        return client.text_to_image(
            prompt=full_prompt,
            model=image_model,
            width=width,
            height=height,
        )

    if provider == "gemini":
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model=image_model,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        for part in getattr(response, "parts", []) or []:
            if getattr(part, "inline_data", None) is not None:
                return Image.open(BytesIO(part.inline_data.data))

        candidates = getattr(response, "candidates", []) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            for part in getattr(content, "parts", []) or []:
                if getattr(part, "inline_data", None) is not None:
                    return Image.open(BytesIO(part.inline_data.data))

        raise RuntimeError("Gemini did not return an image for this prompt.")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.images.generate(
        model=image_model,
        prompt=full_prompt,
        size=IMAGE_SIZE,
        quality=IMAGE_QUALITY,
        n=1,
    )

    image_url = response.data[0].url
    img_bytes = requests.get(image_url, timeout=30).content
    return Image.open(BytesIO(img_bytes))


def _parse_size(size: str) -> tuple[int, int]:
    """Parse WIDTHxHEIGHT into integer dimensions."""
    try:
        width_text, height_text = size.lower().split("x", 1)
        return int(width_text), int(height_text)
    except ValueError as exc:
        raise ValueError("IMAGE_SIZE must be in WIDTHxHEIGHT format, for example 1024x1024.") from exc
