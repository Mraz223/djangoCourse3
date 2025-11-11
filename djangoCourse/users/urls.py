from django.urls import path
from .views import register, profile, custom_logout, register_api, profile

urlpatterns = [
    path("register/", register, name="register"),
    path('profile/', profile, name='profile'),
    path('logout/', custom_logout, name='logout'),
    path('api/register/', register_api, name='register_api'),
    path('api/profile/', profile, name='profile_api'),
]