# vision_tracker_app/vision_tracker_api/models.py

from django.db import models

class VisionCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    focus_value = models.IntegerField(default=100)

    class Meta:
        verbose_name_plural = "Vision Categories"

    def __str__(self):
        return self.name

class MemoryChunk(models.Model):
    text_content = models.TextField()
    chroma_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"MemoryChunk {self.id}: {self.text_content[:50]}..."

    class Meta:
        ordering = ['-created_at']