import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

with open("prompts/system_prompt.txt", "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()


def ask_gemini(question):
    try:
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

    except Exception as e:
        return f"Error: {e}"


def generate_checklist(user_query):
    try:
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

    except Exception as e:
        return f"Error: {e}"