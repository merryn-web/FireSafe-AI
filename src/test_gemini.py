"""
FireSafe-AI
Gemini API Connection Test
"""

import os
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file."
    )

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send test request
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=(
        "You are testing the FireSafe-AI project. "
        "Reply with exactly: Gemini connection successful."
    ),
)

print("=" * 60)
print("FireSafe-AI Gemini Test")
print("=" * 60)

print("\nGemini response:")
print(response.text)

print("\nGemini connection successful!")