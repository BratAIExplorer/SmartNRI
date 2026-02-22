import os
import json
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root or /data/smartnri/
from pathlib import Path as _P
load_dotenv()
for _ep in [_P(__file__).parent.parent/'.env', _P('/data/smartnri/.env')]:
    if _ep.exists():
        load_dotenv(_ep)
        break

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

def list_models():
    client = genai.Client(api_key=GEMINI_KEY)
    print(f"Checking models for API Key: {GEMINI_KEY[:6]}...{GEMINI_KEY[-4:]}")
    try:
        for model in client.models.list():
            print(f"- {model.name} (Supported: {model.supported_actions})")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
