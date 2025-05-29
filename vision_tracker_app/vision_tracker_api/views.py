# vision_tracker_app/vision_tracker_api/views.py

import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
# from django.http import JsonResponse # Not used in LLMChatView directly

# Models and Serializers (unchanged)
from .models import VisionCategory, MemoryChunk
from .serializers import VisionCategorySerializer, MemoryChunkSerializer

# --- New Imports for MemGPT architecture ---
import google.generativeai as genai
from . import tools  # Import our new tools module
import uuid # For generating unique conversation IDs
from asgiref.sync import sync_to_async # Keep this for chat.send_message
# import json # For serializing/deserializing chat history (implicitly used by chat.history potentially)
from .services.firestore_service import firestore_service # Import your firestore_service instance
 

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
    queryset = MemoryChunk.objects.all()
    serializer_class = MemoryChunkSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"MemoryChunk {instance.id} created via API.")
        # In a real implementation, call Firestore and ChromaDB here as you did before.


# --- The Refactored LLMChatView as a Class-Based APIView ---
class LLMChatView(APIView):
    async def dispatch(self, request, *args, **kwargs): # MODIFIED: dispatch is now async
        """
        Override dispatch to be async and await the handler.
        This is necessary because the 'post' method is async.
        """
        self.args = args
        self.kwargs = kwargs
        # Ensure request is initialized before accessing properties like 'method' or 'user'
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            # The standard initial() method in DRF (handling authentication,
            # permissions, throttling) is synchronous.
            # We call it normally, without await, unless specific async
            # authentication/permission classes are in use that modify 'initial'
            # to be async.
            self.initial(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            # Await the handler if it's an async method (like our 'post' method)
            response = await handler(request, *args, **kwargs) # MODIFIED: await the handler

        except Exception as exc:
            response = self.handle_exception(exc)

        # finalize_response is synchronous and expects a standard Response object
        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    async def post(self, request, *args, **kwargs):
        """
        API endpoint for MemGPT-style LLM chat.
        The LLM now decides when to call tools (like searching for memories)
        to build context and provide a response.
        """
        user_message = request.data.get('message')
        if not user_message:
            return Response({'error': 'Message not provided'}, status=status.HTTP_400_BAD_REQUEST)

        conversation_id = request.data.get('conversation_id')
        if not conversation_id:
            conversation_id = str(uuid.uuid4()) # Generate a new ID for a new conversation
            logger.info(f"New conversation started with ID: {conversation_id}")
        else:
            logger.info(f"Continuing conversation with ID: {conversation_id}")

        loaded_history = []
        try:
            # get_conversation_history is already async
            loaded_history = await firestore_service.get_conversation_history(conversation_id)
            logger.info(f"Loaded {len(loaded_history)} messages for conversation {conversation_id}")
        except Exception as e:
            logger.error(f"Failed to load conversation history for {conversation_id}: {e}", exc_info=True)
            # For robustness, we'll proceed with an empty history.

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash', # Or your preferred model
                tools=[tools.recall_memories] # Pass the function directly
            )
            chat = model.start_chat(history=loaded_history, enable_automatic_function_calling=True)

        except Exception as e:
            logger.critical(f"Failed to initialize Gemini model: {e}", exc_info=True)
            return Response({'error': f'Model initialization failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        try:
            logger.info("Sending initial prompt to Gemini...")
            # The google-generativeai SDK's send_message is synchronous,
            # so sync_to_async is correctly used here.
            response_object = await sync_to_async(chat.send_message)(initial_prompt)

            final_text_response = response_object.text
            logger.info("Received final response from Gemini after potential tool calls.")

            try:
                serializable_history = []
                for message in chat.history: # message is of type google.generativeai.types.Content
                    parts_list = []
                    for part in message.parts: # part is of type google.generativeai.types.Part
                        part_dict = {}
                        # Text part
                        if part.text: # Check if text attribute exists and is not empty/None
                            part_dict['text'] = part.text
                        
                        # Function call part
                        # The SDK ensures that a Part will only have one of these (text, inline_data, function_call, etc.)
                        if hasattr(part, 'function_call') and part.function_call:
                            part_dict['function_call'] = {
                                'name': part.function_call.name,
                                'args': dict(part.function_call.args), # .args is a Struct, convert to dict
                            }
                        
                        # Function response part
                        if hasattr(part, 'function_response') and part.function_response:
                             part_dict['function_response'] = {
                                'name': part.function_response.name,
                                'response': dict(part.function_response.response), # .response is a Struct, convert to dict
                            }
                        
                        # Inline data part (e.g., for images - handle if you use them)
                        if hasattr(part, 'inline_data') and part.inline_data:
                            part_dict['inline_data'] = {
                                'mime_type': part.inline_data.mime_type,
                                # Decide how to serialize 'part.inline_data.data' (bytes)
                                # e.g., base64 encode, or store elsewhere and link
                                'data': "SERIALIZED_BLOB_DATA_PLACEHOLDER" 
                            }
                        
                        if part_dict: # Add part_dict only if it's not empty
                            parts_list.append(part_dict)

                    if parts_list: # Add message only if it has parts
                        serializable_history.append({
                            'role': message.role,
                            'parts': parts_list
                        })
                
                # Now, serializable_history is a list of dicts
                if serializable_history: # Only save if there's something to save
                    await firestore_service.save_conversation_history(conversation_id, serializable_history)
                    logger.info(f"Saved updated chat history for conversation {conversation_id}.")
                else:
                    logger.info(f"No serializable history to save for conversation {conversation_id}.")

            except Exception as e:
                logger.error(f"Failed to serialize or save conversation history for {conversation_id}: {e}", exc_info=True)

            return Response({
                'response': final_text_response,
                'conversation_id': conversation_id # Return the conversation ID
            })

        except Exception as e:
            logger.error(f"An error occurred during the chat session: {e}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)