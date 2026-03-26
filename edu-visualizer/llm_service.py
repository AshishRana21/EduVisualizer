"""Text generation service using Gemini or OpenAI."""
import os

from google import genai
from google.genai import types
from openai import OpenAI

from provider_config import get_llm_model, get_llm_provider

SYSTEM_PROMPT = """You are an expert educator. When given a concept, respond with:
1. A concise definition (2-3 sentences)
2. Key points (3-5 bullet points)
3. A real-world analogy to make it memorable
4. A suggested image prompt (one sentence, vivid and educational) prefixed with IMAGE_PROMPT:

Keep the tone clear and engaging for students."""


def generate_explanation(concept: str, level: str = "high school") -> dict:
    """
    Generate a structured explanation for an educational concept.
    Returns dict with keys: raw, image_prompt
    """
    user_msg = f"Explain the concept: '{concept}' for a {level} student."
    provider = get_llm_provider()
    llm_model = get_llm_model()

    if provider == "gemini":
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model=llm_model,
            contents=user_msg,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
                max_output_tokens=600,
            ),
        )
        raw = (response.text or "").strip()
    else:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
            max_tokens=600,
        )
        raw = (response.choices[0].message.content or "").strip()

    return _parse_response(raw, concept)


def _parse_response(text: str, concept: str) -> dict:
    """Parse the LLM response into structured fields."""
    lines = text.strip().splitlines()

    image_prompt = f"Educational diagram illustrating {concept}, clean infographic style"
    body_lines = []

    for line in lines:
        if line.strip().startswith("IMAGE_PROMPT:"):
            image_prompt = line.split("IMAGE_PROMPT:", 1)[-1].strip()
        else:
            body_lines.append(line)

    return {
        "raw": "\n".join(body_lines).strip(),
        "image_prompt": image_prompt,
    }
