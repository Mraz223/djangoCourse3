from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Панель администратора DjangoCourse"
admin.site.site_title = "DjangoCourse admin"
admin.site.index_title = "Управление сайтом DjangoCourse"





def home(request):
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  
    path('courses/', include('courses.urls')),
    path('tasks/', include('tasks.urls')),
    path('users/', include('users.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('videos/', include('videos.urls')),
    path('accounts/login/', LoginView.as_view(
        redirect_authenticated_user=True,
        next_page='home'), name='login'),
    path('', include('core.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
