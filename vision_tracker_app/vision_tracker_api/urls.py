# vision_tracker_app/vision_tracker_api/urls.py

from django.urls import path
from .views import (
    VisionCategoryListView,
    VisionCategoryDetailView,
    test_firestore_connection,
    test_chroma_embedding_and_query,
    llm_chat_view,
    MemoryChunkCreateView # NEW: Import the new MemoryChunk view
)

urlpatterns = [
    path('vision-data/', VisionCategoryListView.as_view(), name='vision_data_list'),
    path('vision-data/<int:pk>/', VisionCategoryDetailView.as_view(), name='vision_data_detail'),
    path('test-firestore/', test_firestore_connection, name='test_firestore'),
    path('test-chroma/', test_chroma_embedding_and_query, name='test_chroma'),
    path('llm-chat/', llm_chat_view, name='llm_chat'),
    path('memories/', MemoryChunkCreateView.as_view(), name='memory_chunk_create'), 
]