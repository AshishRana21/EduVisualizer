"""Compose a flashcard image by overlaying concept text onto the generated image."""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io


def build_flashcard(concept: str, explanation: str, visual: Image.Image) -> Image.Image:
    """
    Overlay concept title and a short explanation onto the visual image.
    Returns a composite PIL Image ready for display or download.
    """
    card = visual.copy().convert("RGBA")
    width, height = card.size

    # Semi-transparent footer banner
    banner_h = int(height * 0.28)
    overlay = Image.new("RGBA", (width, banner_h), (0, 0, 0, 180))
    card.paste(overlay, (0, height - banner_h), overlay)

    draw = ImageDraw.Draw(card)

    # Try to load a nicer font, fall back to default
    try:
        title_font = ImageFont.truetype("arial.ttf", size=36)
        body_font = ImageFont.truetype("arial.ttf", size=22)
    except OSError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Title
    title = concept.upper()
    draw.text((20, height - banner_h + 12), title, font=title_font, fill=(255, 220, 50, 255))

    # Body text — wrap to fit width
    short_text = _truncate(explanation, max_chars=220)
    wrapped = textwrap.fill(short_text, width=55)
    draw.text((20, height - banner_h + 58), wrapped, font=body_font, fill=(240, 240, 240, 255))

    return card.convert("RGB")


def image_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def _truncate(text: str, max_chars: int) -> str:
    # Strip markdown bullets for cleaner display
    clean = " ".join(
        line.lstrip("•-* ").strip()
        for line in text.splitlines()
        if line.strip()
    )
    return clean[:max_chars] + ("…" if len(clean) > max_chars else "")
