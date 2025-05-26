# vision_tracker_app/vision_tracker_api/services/gemini_service.py

import google.generativeai as genai
import os
from django.conf import settings # Import settings to access GEMINI_API_KEY

# Configure the API key from Django settings
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_embedding(text: str) -> list:
    """
    Generates an embedding for the given text using Google's embedding model.
    """
    if not settings.GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY is not configured.")
        return [] # Return empty list or raise an error

    try:
        # Use the embedding model configured with the API key
        # The task_type is important for embedding quality
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document" # Or "retrieval_query" depending on use case
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return [] 