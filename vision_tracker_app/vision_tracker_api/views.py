# vision_tracker_backend/vision_tracker_api/views.py

from django.http import JsonResponse

def hello_world(request):
    return JsonResponse({"message": "Hello from Django Backend!"})