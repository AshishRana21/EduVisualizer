"""
Multimodal GenAI Education Visualizer
Streamlit app that combines LLM explanations with AI-generated visuals
to produce educational flashcards.
"""
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from llm_service import generate_explanation
from image_service import generate_image
from flashcard import build_flashcard, image_to_bytes
from provider_config import (
    get_image_model,
    get_image_provider,
    get_llm_model,
    get_llm_provider,
    has_configured_image_provider,
    has_configured_llm_provider,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduVisualizer – Concept Flashcards",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 EduVisualizer")
st.caption("Turn any concept into an AI-generated explanation + visual flashcard")

# ── Sidebar controls ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")
    level = st.selectbox(
        "Student level",
        ["elementary school", "middle school", "high school", "undergraduate", "graduate"],
        index=2,
    )
    show_raw = st.checkbox("Show raw LLM output", value=False)
    st.divider()
    st.markdown("**Models in use**")
    llm_provider = get_llm_provider() or "not configured"
    image_provider = get_image_provider() or "not configured"
    st.code(
        f"LLM Provider: {llm_provider}\n"
        f"LLM Model: {get_llm_model()}\n"
        f"Image Provider: {image_provider}\n"
        f"Image Model: {get_image_model()}"
    )

# ── Main input ────────────────────────────────────────────────────────────────
concept = st.text_input(
    "Enter an educational concept",
    placeholder="e.g. Photosynthesis, Pythagorean Theorem, Supply and Demand…",
)

col_gen, col_ex = st.columns([1, 4])
generate_btn = col_gen.button("✨ Generate", type="primary", disabled=not concept)

# Example concepts
with col_ex:
    examples = ["Photosynthesis", "Newton's Laws", "Supply & Demand", "DNA Replication", "Pythagorean Theorem"]
    chosen = st.pills("Quick examples", examples, label_visibility="collapsed")
    if chosen:
        concept = chosen

# ── Generation pipeline ───────────────────────────────────────────────────────
if generate_btn or (chosen and chosen != st.session_state.get("last_example")):
    if chosen:
        st.session_state["last_example"] = chosen

    if not has_configured_llm_provider():
        st.error("Set `GEMINI_API_KEY` or `OPENAI_API_KEY` in your `.env` file for explanations.")
        st.stop()

    if not has_configured_image_provider():
        st.error("Set `HUGGINGFACE_API_KEY`, `GEMINI_API_KEY`, or `OPENAI_API_KEY` in your `.env` file for images.")
        st.stop()

    with st.spinner("🧠 Generating explanation…"):
        try:
            result = generate_explanation(concept, level)
        except Exception as e:
            st.error(f"LLM error: {e}")
            st.stop()

    with st.spinner("🎨 Generating visual…"):
        try:
            visual = generate_image(result["image_prompt"])
        except Exception as e:
            st.error(f"Image generation error: {e}")
            st.stop()

    with st.spinner("🃏 Building flashcard…"):
        flashcard = build_flashcard(concept, result["raw"], visual)

    # ── Display results ───────────────────────────────────────────────────────
    st.divider()
    left, right = st.columns(2)

    with left:
        st.subheader("📖 Explanation")
        st.markdown(result["raw"])
        if show_raw:
            with st.expander("Image prompt sent to the image model"):
                st.code(result["image_prompt"])

    with right:
        st.subheader("🃏 Flashcard")
        st.image(flashcard, use_container_width=True)
        st.download_button(
            label="⬇ Download Flashcard",
            data=image_to_bytes(flashcard),
            file_name=f"{concept.replace(' ', '_')}_flashcard.png",
            mime="image/png",
        )
