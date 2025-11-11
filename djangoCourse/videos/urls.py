from django.urls import path
from .views import video_list, video_detail, video_list_api

urlpatterns = [
    path('', video_list, name='video_list'),
    path('video/<int:video_id>/', video_detail, name='video_detail'),
    path('api/videos/', video_list_api, name='video_list_api'),
]