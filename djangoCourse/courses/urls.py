from django.urls import path
from .views import course_list
from .views import video_list

urlpatterns = [
    path('', course_list, name='course_list'),
    path("videos/", video_list, name="video_list"),
]
