# vision_tracker_app/vision_tracker_api/urls.py

from django.urls import path
from .views import (
    VisionCategoryListView,
    VisionCategoryDetailView,
    LLMChatView, 
    MemoryChunkCreateView
)

urlpatterns = [
    path('vision-data/', VisionCategoryListView.as_view(), name='vision_data_list'),
    path('vision-data/<int:pk>/', VisionCategoryDetailView.as_view(), name='vision_data_detail'),
    path('llm-chat/', LLMChatView.as_view(), name='llm_chat'), # <--- CHANGED: Use LLMChatView.as_view()
    path('memories/', MemoryChunkCreateView.as_view(), name='memory_chunk_create'),
]