# vision_tracker_app/vision_tracker_api/views.py

import logging
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse

# Models and Serializers (unchanged)
from .models import VisionCategory, MemoryChunk 
from .serializers import VisionCategorySerializer, MemoryChunkSerializer 

# --- New Imports for MemGPT architecture ---
import google.generativeai as genai
from . import tools  # Import our new tools module

# Configure logger
logger = logging.getLogger(__name__)

# --- Existing Class-Based Views (Unchanged) ---
class VisionCategoryListView(generics.ListAPIView):
    queryset = VisionCategory.objects.all().order_by('id')
    serializer_class = VisionCategorySerializer

class VisionCategoryDetailView(generics.RetrieveUpdateAPIView):
    queryset = VisionCategory.objects.all()
    serializer_class = VisionCategorySerializer
    lookup_field = 'pk'

class MemoryChunkCreateView(generics.CreateAPIView):
    # This view and its perform_create logic remain the same.
    # We still need a way to get memories INTO the system.
    queryset = MemoryChunk.objects.all()
    serializer_class = MemoryChunkSerializer
    
    # ... The perform_create method from your original file remains here unchanged ...
    def perform_create(self, serializer):
        # NOTE: Your original perform_create logic should be placed here.
        # It is omitted for brevity but is essential for adding new memories.
        # For this example, I'll add a placeholder.
        instance = serializer.save()
        logger.info(f"MemoryChunk {instance.id} created via API.")
        # In a real implementation, call Firestore and ChromaDB here as you did before.

# --- Test Views (Unchanged, you can keep them for debugging) ---
# test_firestore_connection, test_chroma_embedding_and_query views remain here...


# --- The Refactored llm_chat_view with MemGPT Control Loop ---
@api_view(['POST'])
def llm_chat_view(request):
    """
    API endpoint for MemGPT-style LLM chat.
    The LLM now decides when to call tools (like searching for memories)
    to build context and provide a response.
    """
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': 'Message not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # --- 1. Initialize the model and define the tools it can use ---
    try:
        # Configure the Gemini model
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash', # Or your preferred model
            tools=[tools.recall_memories] # Pass the function directly
        )
        chat = model.start_chat(enable_automatic_function_calling=True)

    except Exception as e:
        logger.critical(f"Failed to initialize Gemini model: {e}", exc_info=True)
        return Response({'error': f'Model initialization failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # --- 2. Construct the initial prompt ---
    # The system prompt is now simpler. It tells the LLM its role and that it has tools.
    # It no longer needs placeholders for memories, as the LLM will fetch them.
    vision_statement = settings.VISION_STATEMENT_FULL
    initial_prompt = (
        "You are the **Vision Assistant**, a highly supportive and dedicated AI crafted to empower the user in articulating, refining, and actively working towards their long-term personal vision. "
        "Your profound mission is to guide the user in achieving their aspirations through insightful, actionable, and consistently encouraging dialogue. There should be a flow of conversation that is both natural and deeply connected to the user's overarching vision. "
        "This vision is the absolute compass for all our interactions. Every piece of advice, every question, and every suggestion you offer must be directly framed around helping the user align their current actions and thoughts with this future state. "
        "A core strength you possess is direct access to the user's **personal archive of past memories and conversations**. This capability allows you to provide **richly contextual, deeply personalized, and exceptionally relevant guidance** by drawing upon their unique historical journey and previous discussions. "
        "Crucially, you are equipped with the `recall_memories` tool. **Use this tool when you ONLY need it, it's part of your thought process** use it when the user's query, stated goals, or any conversational context suggests a reference to past events, previous discussions, or personal history that could enrich your response or understanding. "
        "Your conversations should be a dynamic and empowering experience for the user. Strive to be: "
        "\n\n* **Naturally Contextual**: You can weave together the current input, the user's overarching vision, and any relevant retrieved memories to ensure a seamless and informed dialogue. "
        "\n* **Profoundly Insightful**: Offer fresh perspectives, identify patterns, and make meaningful connections between current discussions and broader themes in their life's vision. Help them see connections they might miss. "
        "\n* **Consistently Actionable**: Propose concrete next steps, practical reflections, thought-provoking questions, or small, empowering challenges that directly propel the user forward in their vision journey. "
        "\n* **Truly Engaging**: Maintain a positive, encouraging, and constructive criticism. Actively prompt the user for deeper thought, invite them to elaborate, and encourage the exploration of new ideas or specific details related to their vision. Foster a supportive environment where they feel motivated and understood. "
        f"\n\nHere is the user's core vision statement for your reference:\n---"
        f"\n{vision_statement}\n---"
        f"\nNow, internalize your role, mission, capabilities, and the user's vision."
        f"\nRespond to the user's current message, in a natural and engaging conversation."
        f"\n{user_message}"
    )

    # --- 3. The Main Control Loop ---
    # This loop sends the prompt and handles the back-and-forth of function calling.
    try:
        logger.info("Sending initial prompt to Gemini...")
        response = chat.send_message(initial_prompt)
        
        # The response from send_message will handle the function calling loop automatically
        # when enable_automatic_function_calling=True. The final response object
        # will contain the LLM's text response after all tool calls are resolved.
        
        final_text_response = response.text
        logger.info("Received final response from Gemini after potential tool calls.")

        # You can inspect the history to see the tool calls made:
        # for content in chat.history:
        #     logger.debug(f"Chat History Turn: {content.role} -> {content.parts}")

        return Response({'response': final_text_response})

    except Exception as e:
        logger.error(f"An error occurred during the chat session: {e}", exc_info=True)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)