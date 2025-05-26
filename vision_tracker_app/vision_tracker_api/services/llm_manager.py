# vision_tracker_app/vision_tracker_api/services/llm_manager.py

import google.generativeai as genai
from django.conf import settings # To access GEMINI_API_KEY

# Configure the Gemini API key
genai.configure(api_key=settings.GEMINI_API_KEY)

class LLMManager:
    _instance = None
    _model = None # Use _model for consistency

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMManager, cls).__new__(cls)
            cls._instance._initialize_llm()
        return cls._instance

    def _initialize_llm(self):
        """Initializes the Gemini GenerativeModel."""
        # Use _model as a private instance variable
        self._model = genai.GenerativeModel('gemini-1.5-flash')
        print("DEBUG: Gemini flash model initialized in LLMManager.")

    # New method to generate embeddings
    def generate_embedding(self, text: str):
        """Generates an embedding for the given text using Gemini's embedding model."""
        try:
            # Ensure the embedding model is used. 'embedding-001' is for embeddings.
            model = genai.GenerativeModel('embedding-001')
            embedding_response = model.embed_content(content=text)
            return embedding_response['embedding']
        except Exception as e:
            print(f"ERROR: Failed to generate embedding for text: {e}")
            return None

    # Renamed from process_user_input to reflect its new role
    def generate_text_response(self, full_prompt: str) -> str:
        """
        Sends a complete prompt to Gemini and returns the text response.
        This method assumes the prompt already contains all necessary context (like memories).
        """
        if not full_prompt.strip():
            return "Error: Prompt cannot be empty."

        try:
            print("DEBUG: Sending prompt to Gemini flash for response generation...")
            response = self._model.generate_content(full_prompt) # Use self._model here
            
            response_text = ""
            if response and response.text:
                response_text = response.text
            elif response and response.parts:
                for part in response.parts:
                    if hasattr(part, 'text'):
                        response_text += part.text
            print(f"DEBUG: Received response from Gemini Flash (first 100 chars): {response_text[:100]}...")
            return response_text
        except Exception as e:
            print(f"ERROR: Failed to get response from Gemini Flash: {e}")
            return f"I apologize, but I encountered an error communicating with the AI: {e}"

# Make it a singleton for easy access throughout the Django app
llm_manager = LLMManager()