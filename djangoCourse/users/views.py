from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Achievement
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from .models import Profile
from .forms import ProfileUpdateForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class SimpleRegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")  # ДОБАВЬ ЭТО
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Your password must contain at least 8 characters and can't be entirely numeric."
    )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages)
        return password
    
    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']  
        password = self.cleaned_data['password']
        user = User.objects.create_user(username=username, email=email, password=password)  # ДОБАВЬ EMAIL
        return user


def register(request):
    if request.method == "POST":
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
           
            try:
                send_mail(
                    'Добро пожаловать в DjangoCourse! 🐍',
                    f'''Привет, {user.username}!

Добро пожаловать в DjangoCourse! Теперь ты можешь:
• Смотреть видео-уроки по Python
• Решать практические задачи
• Получать достижения
• Сохранять свой прогресс

Начни обучение: http://127.0.0.1:8000/

Удачи в изучении программирования! 🚀

С уважением,
Команда DjangoCourse''',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],  
                    fail_silently=False,
                )
                print(f"✅ Email отправлен новому пользователю: {user.username}")
            except Exception as e:
                print(f"⚠️ Email не отправлен: {e}")
            
            return redirect("login")
    else:
        form = SimpleRegisterForm()
    return render(request, "registration/register.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    achievements = request.user.achievements.all()
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'users/profile.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
        'achievements': achievements  
    })


@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            print("Raw body:", body)
            
            if not body:
                return JsonResponse({'status': 'error', 'message': 'Empty body'})
            
            data = json.loads(body)
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            
            if not username or not email or not password:
                return JsonResponse({'status': 'error', 'message': 'Все поля обязательны'})
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Пользователь уже существует'})
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            Profile.objects.create(user=user)
            
            return JsonResponse({'status': 'success', 'user_id': user.id})
            
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': f'JSON error: {str(e)}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'})