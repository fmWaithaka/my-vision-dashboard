# vision_tracker_app/vision_tracker_api/serializers.py

from rest_framework import serializers
from .models import VisionCategory, MemoryChunk

class VisionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VisionCategory
        fields = ['id', 'name', 'focus_value'] # Specify fields to include in API response

class MemoryChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryChunk
        fields = '__all__'
        read_only_fields = ['created_at']