"""Shared configuration helpers for selecting AI providers."""
import os


SUPPORTED_LLM_PROVIDERS = ("gemini", "openai")
SUPPORTED_IMAGE_PROVIDERS = ("huggingface", "gemini", "openai")


def get_llm_provider() -> str | None:
    """Return the LLM provider selected by available API keys."""
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    return None


def get_image_provider() -> str | None:
    """Return the image provider selected by available API keys."""
    if os.getenv("HUGGINGFACE_API_KEY"):
        return "huggingface"
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    return None


def has_configured_llm_provider() -> bool:
    return get_llm_provider() is not None


def has_configured_image_provider() -> bool:
    return get_image_provider() is not None


def get_llm_model() -> str:
    provider = get_llm_provider()
    default_model = "gemini-2.5-flash" if provider == "gemini" else "gpt-4o"
    return os.getenv("LLM_MODEL", default_model)


def get_image_model() -> str:
    provider = get_image_provider()
    if provider == "huggingface":
        default_model = "black-forest-labs/FLUX.1-schnell"
    elif provider == "gemini":
        default_model = "gemini-2.5-flash-image"
    else:
        default_model = "dall-e-3"
    return os.getenv("IMAGE_MODEL", default_model)
