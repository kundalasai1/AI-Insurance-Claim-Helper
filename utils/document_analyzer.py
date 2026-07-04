import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_document(image_path):

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