from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TaskTests(TestCase):
    def setUp(self):
        """Создаем тестового пользователя"""
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass')
    
    def test_task_list_page(self):
        """Тест страницы списка задач"""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задачи')  
    
    def test_task_list_works_without_login(self):
        """Тест что задачи доступны без авторизации"""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)  
    
    def test_task_list_with_login(self):
        """Тест что задачи работают с авторизацией"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)