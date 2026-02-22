import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_notes(combined_text):
    prompt = f"""
    I am providing a transcript and OCR text from a lecture. 
    Please create structured notes including:
    1. A high-level summary.
    2. Detailed bullet points.
    3. Any formulas or definitions found in either the audio or on the screen.

    {combined_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001", # Or your preferred OpenRouter model
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"