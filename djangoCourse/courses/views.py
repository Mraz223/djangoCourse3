from django.shortcuts import render
from .models import Course
from django.contrib.auth.decorators import login_required

def course_list(request):
    courses = [
        {'title': 'Python для начинающих', 'description': 'Основы программирования на Python'},
        {'title': 'Django веб-разработка', 'description': 'Создание сайтов на Django'},
        {'title': 'Базы данных', 'description': 'Работа с SQL и ORM'},
    ]
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required
def video_list(request):
    course = Course.objects.all()
    return render(request, 'videos/video_list.html', {'course': course})