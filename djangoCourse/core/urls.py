from django.urls import path
from .views import video_list_view
from . import views


urlpatterns = [
    path('videos/', video_list_view, name='video-list'),
    path('reviews/', views.reviews_view, name='reviews'),
    
]
