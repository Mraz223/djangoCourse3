from django.urls import path
from .views import task_list, task_detail, daily_task, task_list_api, check_solution_api

urlpatterns = [
    path('', task_list, name='task_list'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path("daily/", daily_task, name="daily_task"),
    path('api/tasks/', task_list_api, name='task_list_api'),
    path('api/tasks/<int:task_id>/check/', check_solution_api, name='check_solution_api'),
]
