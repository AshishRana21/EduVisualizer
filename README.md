# EduVisualizer

EduVisualizer is a **Streamlit-based educational application** that converts a learning concept into a **student-friendly explanation, an AI-generated educational visual, and a downloadable flashcard image**. The system integrates **Large Language Models (LLMs)** with **Image Generation APIs** to produce **multimodal educational content** that helps students understand concepts visually and textually. The current configuration is optimized for **low-cost AI usage**, using **Gemini API for text explanations** and **Hugging Face Inference API for image generation**.

## Features

* Explain any academic concept in simple language
* Adjust explanations for different student levels
* Generate an educational image based on the explanation
* Combine text and image into a flashcard
* Download the final flashcard as a PNG image
* Support multiple AI providers for flexibility

## Tech Stack

* Python
* Streamlit
* Gemini API or OpenAI API for LLM responses
* Hugging Face Inference API, Gemini, or OpenAI for image generation
* Pillow library for flashcard composition

## Project Structure

```
edu-visualizer/
├── app.py
├── llm_service.py
├── image_service.py
├── flashcard.py
├── provider_config.py
├── requirements.txt
├── .env
└── README.md
```

## How It Works

1. The user enters an educational concept such as **Photosynthesis**.
2. `llm_service.py` generates a structured explanation and an image prompt.
3. `image_service.py` creates an educational image using the generated prompt.
4. `flashcard.py` overlays the concept title and explanation on the image.
5. The final flashcard is displayed in Streamlit and can be downloaded by the user.

## Setup

### 1. Clone the Repository

```
git clone https://github.com/yourusername/edu-visualizer.git
cd edu-visualizer
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file and add your API keys:

```
GEMINI_API_KEY=your_gemini_key
HUGGINGFACE_API_KEY=your_huggingface_token
OPENAI_API_KEY=

LLM_MODEL=gemini-2.5-flash
IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
IMAGE_SIZE=1024x1024
IMAGE_QUALITY=standard
```

**Notes**

* `GEMINI_API_KEY` is used for text explanations by default.
* `HUGGINGFACE_API_KEY` is used for image generation by default.
* `OPENAI_API_KEY` is optional and only required if OpenAI models are used.

## Run the Application

```
streamlit run app.py
```

If Streamlit is not recognized:

```
python -m streamlit run app.py
```

After running the command, open the local URL displayed in the terminal, usually:

```
http://localhost:8501
```

## Provider Selection Logic

### LLM Provider Priority

1. Gemini if `GEMINI_API_KEY` is available
2. OpenAI if `OPENAI_API_KEY` is available

### Image Provider Priority

1. Hugging Face if `HUGGINGFACE_API_KEY` is available
2. Gemini if `GEMINI_API_KEY` is available
3. OpenAI if `OPENAI_API_KEY` is available

## Example Use Cases

* Science concept flashcards
* Math theorem summaries
* Economics revision cards
* Classroom visual aids
* Student self-study material

## Troubleshooting

### 429 RESOURCE_EXHAUSTED

This error means the API quota has been exceeded.

* If the error mentions **Gemini**, the Gemini quota is exhausted.
* If the error comes from **Hugging Face**, verify the Hugging Face token and model availability.

### Streamlit Not Recognized

Run the application using:

```
python -m streamlit run app.py
```

### Missing API Key Errors

Ensure the `.env` file contains valid API keys and there are no extra spaces.

## Future Improvements

* Add history for previously generated flashcards
* Support exporting flashcards as PDF
* Add subject-specific prompt templates
* Add offline fallback visuals
* Improve flashcard layout and typography

## License

This project is intended for **educational purposes**. 
You may add a license such as the **MIT License** before publishing publicly.

## Author

**Ashish Rana , Ujjwal Mehta, Jay Patidar, Ravi Patidar**
