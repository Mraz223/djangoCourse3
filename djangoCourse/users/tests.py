from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class UserTests(TestCase):
    def test_register_page(self):
        """Тест страницы регистрации"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Регистрация')
    
    def test_user_registration(self):
        """Тест регистрации пользователя"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  
        
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
    
    def test_profile_creation(self):
        """Тест создания профиля"""
        user = User.objects.create_user('testuser', 'test@example.com', 'testpass')
        
        profile = Profile.objects.create(user=user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user.username, 'testuser')

    def test_login_page(self):
        """Тест страницы входа"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вход')
    
    def test_profile_page_requires_login(self):
        """Тест что профиль требует авторизации"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  