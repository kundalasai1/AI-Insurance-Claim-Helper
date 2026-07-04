import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Load system prompt
try:
    with open("prompts/system_prompt.txt", "r", encoding="utf-8") as file:
        SYSTEM_PROMPT = file.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "You are a helpful insurance assistant."


@st.cache_resource
def get_gemini_client():
    """Initialize Gemini client with lazy loading and error handling"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "❌ GEMINI_API_KEY not found. "
            "Please set the GEMINI_API_KEY environment variable in Streamlit Cloud secrets or .env file."
        )
    
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        raise ValueError(f"Failed to initialize Gemini client: {str(e)}")


def ask_gemini(question):
    """Send a question to Gemini and get a response"""
    try:
        client = get_gemini_client()
        
        prompt = f"""
{SYSTEM_PROMPT}

User Question:
{question}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except ValueError as ve:
        return f"⚠️ Configuration Error: {str(ve)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def generate_checklist(user_query):
    """Generate a checklist for insurance claim based on user query"""
    try:
        client = get_gemini_client()
        
        prompt = f"""
You are an Insurance Claim Expert.

The user describes an incident.

Your task:
1. Identify the insurance claim type.
2. List the required documents.
3. Explain why each document is required.

User:
{user_query}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except ValueError as ve:
        return f"⚠️ Configuration Error: {str(ve)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"