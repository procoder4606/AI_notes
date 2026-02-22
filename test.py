import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# 2. Initialize the client (Note the 'base_url')
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

try:
    # 3. Call the model
    # Note: OpenRouter uses "provider/model" format
    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-001", # You can use Gemini here too!
        messages=[
            {"role": "user", "content": "Explain photosynthesis in 3 lines."}
        ]
    )
    
    print("--- Success! ---")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"Error: {e}")