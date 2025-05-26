# vision_tracker_app/vision_tracker_api/views.py

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VisionCategory, MemoryChunk 
from .serializers import VisionCategorySerializer, MemoryChunkSerializer 
from django.conf import settings
from rest_framework import status

# Firebase Imports
import firebase_admin
from firebase_admin import firestore
from django.http import JsonResponse

from .services.chroma_service import chroma_service
from .services.llm_manager import llm_manager

class VisionCategoryListView(generics.ListAPIView):
    """
    API endpoint to list all Vision Categories.
    """
    queryset = VisionCategory.objects.all().order_by('id')
    serializer_class = VisionCategorySerializer

class VisionCategoryDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve or update a single Vision Category.
    """
    queryset = VisionCategory.objects.all()
    serializer_class = VisionCategorySerializer
    lookup_field = 'pk'


# ---  test_firestore_connection view  ---
def test_firestore_connection(request):
    """
    API endpoint to test Firebase Firestore connection.
    Adds a dummy document and tries to retrieve it.
    """
    print(f"Gemini API Key loaded in views.py: {'Yes' if settings.GEMINI_API_KEY else 'No'}")

    try:
        if not firebase_admin._apps:
            return JsonResponse({"status": "error", "message": "Firebase app not initialized."}, status=500)

        db = firestore.client()
        test_doc_ref = db.collection('test_collection').document('test_doc')
        test_doc_ref.set({'message': 'Hello from Django and Firestore test!'})

        doc = test_doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return JsonResponse({"status": "success", "message": "Firestore connected!", "data": data})
        else:
            return JsonResponse({"status": "error", "message": "Firestore document not found after write."}, status=500)
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Firestore/Gemini test failed: {e}"}, status=500)


# ---  test_chroma_embedding_and_query view  ---
def test_chroma_embedding_and_query(request):
    """
    API endpoint to test ChromaDB's add and query functionality
    using Gemini embeddings.
    """
    test_doc_id = "test_memory_1"
    test_text = "My long-term vision is to foster impactful leadership and continuous personal growth."
    query_text = "How can I improve my leadership skills?"

    try:
        # 1. Add a test memory to ChromaDB
        chroma_service.add_memory(
            doc_id=test_doc_id,
            document_text=test_text,
            metadata={"source": "test_view", "category": "Vision"}
        )

        # 2. Query ChromaDB for related memories
        results = chroma_service.query_memories(
            query_text=query_text,
            n_results=2
        )

        if results:
            return JsonResponse({
                "status": "success",
                "message": "ChromaDB add and query successful!",
                "added_document": {"id": test_doc_id, "text": test_text},
                "query_results": results
            })
        else:
            return JsonResponse({
                "status": "warning",
                "message": "ChromaDB add successful, but no results found for query (might be expected for this test data)."
            })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"ChromaDB test failed: {e}"
        }, status=500)

@api_view(['POST'])
def llm_chat_view(request):
    """
    API endpoint for LLM chat.
    Accepts a 'message' from the user, retrieves relevant memories,
    and sends both to the LLM for a contextual response.
    """
    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': 'Message not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        print(f"DEBUG: Querying ChromaDB with user message: '{user_message}'")
        relevant_memories = chroma_service.query_memories(user_message)

        context_memories = ""
        if relevant_memories:
            context_memories = "\n\nRelevant Past Memories (from your personal context):\n"
            for i, mem in enumerate(relevant_memories):
                context_memories += f"- Memory {i+1} (Score: {mem.get('distance', 'N/A'):.2f}): {mem.get('document', 'No content')}\n"
            print(f"DEBUG: Retrieved relevant memories:\n{context_memories}")
        else:
            print("DEBUG: No relevant memories found for the user message.")

        vision_statement = settings.VISION_STATEMENT_FULL

        system_instruction = (
            "You are the 'Vision Assistant', a helpful and encouraging AI. "
            "Your primary role is to help the user articulate, refine, and achieve their long-term vision. "
            "You are designed to be supportive, insightful, and action-oriented. "
            "You should use the provided 'Full Personal Vision Statement' and 'Relevant Past Memories' to provide context-aware responses, "
            "offer guidance, set actionable goals, and help the user track progress. "
            "Always be positive and focused on the user's growth."
        )

        full_prompt = (
            f"{system_instruction}\n\n"
            f"Full Personal Vision Statement:\n{vision_statement}\n"
            f"{context_memories}\n\n"
            f"User's Current Query:\n{user_message}\n\n"
            "Based on the user's query, their vision statement, and any relevant past memories, "
            "provide a helpful, insightful, and actionable response. "
            "If appropriate, suggest a next step or an actionable goal aligned with their vision."
        )

        print("DEBUG: Sending prompt to Gemini Pro...")
        # Use the LLM Manager to get a response
        llm_response_content = llm_manager.generate_text_response(full_prompt) 
        print("DEBUG: Received response from Gemini Pro.")

        return Response({'response': llm_response_content})

    except Exception as e:
        print(f"ERROR in llm_chat_view: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class MemoryChunkCreateView(generics.CreateAPIView):
    """
    API endpoint to create a new MemoryChunk.
    Automatically saves to Firebase Firestore and adds an embedding to ChromaDB.
    """
    queryset = MemoryChunk.objects.all()
    serializer_class = MemoryChunkSerializer

    def perform_create(self, serializer):
        instance = serializer.save() # First, save to Django ORM (and implicitly to Firestore if hooks were here)

        try:
            # 1. Save to Firebase Firestore (more robust storage than Django ORM for this use case)
            db = firestore.client()
            # Use instance.id as the document ID in Firestore for easy lookup
            # Convert the Django model instance to a dictionary for Firestore
            memory_data = {
                'text_content': instance.text_content,
                'created_at': instance.created_at.isoformat(), # Convert datetime to ISO format string
                # Add other fields from MemoryChunk model if desired, e.g., 'category'
                # 'category': instance.category if instance.category else None,
            }
            firestore_doc_ref = db.collection('memory_chunks').document(str(instance.id))
            firestore_doc_ref.set(memory_data)
            print(f"DEBUG: MemoryChunk {instance.id} saved to Firestore.")

            # 2. Add embedding to ChromaDB
            # Use instance.id as the doc_id for ChromaDB
            chroma_service.add_memory(
                doc_id=str(instance.id), # ChromaDB IDs must be strings
                document_text=instance.text_content,
                metadata={
                    "created_at": instance.created_at.isoformat(),
                    "source": "MemoryChunk API",
                    # Add other metadata if relevant, e.g., user_id, category
                }
            )
            print(f"DEBUG: MemoryChunk {instance.id} embedding added to ChromaDB.")

        except Exception as e:
            # Log the error, but still allow the Django ORM save to proceed
            print(f"ERROR: Failed to save MemoryChunk {instance.id} to Firestore or ChromaDB: {e}")
            # Depending on criticality, you might want to raise an exception here
            # or have a retry mechanism. For now, just print.