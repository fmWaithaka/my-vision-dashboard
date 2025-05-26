# vision_tracker_app/vision_tracker_api/admin.py

from django.contrib import admin
from .models import VisionCategory

admin.site.register(VisionCategory)