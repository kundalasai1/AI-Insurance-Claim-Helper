"""
Test script for Gemini API
Run locally to test API connectivity
"""

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not set. Add it to .env file")
    exit(1)

try:
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say Hello"
    )
    
    print("✅ API Test Successful!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")