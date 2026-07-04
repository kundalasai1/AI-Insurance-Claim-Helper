import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()


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


def analyze_document(image_path):
    """Analyze insurance document image and extract key information"""
    try:
        client = get_gemini_client()
        
        image = Image.open(image_path)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                """
                You are an Insurance Document Verification Assistant.

                Analyze the uploaded document.

                Tell:
                1. Document Type
                2. Important Information Present
                3. Missing Information (if any)
                4. Is the document suitable for insurance claim?
                """,
                image
            ]
        )

        return response.text
    
    except ValueError as ve:
        return f"⚠️ Configuration Error: {str(ve)}"
    except FileNotFoundError:
        return f"❌ Error: Image file not found at {image_path}"
    except Exception as e:
        return f"❌ Error analyzing document: {str(e)}"