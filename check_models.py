import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Fetching available models...")
for model in client.models.list():
    # Only print models that support generating content (bypasses embedding-only models)
    if "generateContent" in model.supported_actions:
        print(model.name)