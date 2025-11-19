from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Achievement, Profile
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import ProfileUpdateForm, SimpleRegisterForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages





def register(request):
    if request.method == "POST":
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # UserCreationForm создаёт нового пользователя

            # === Отправка приветственного письма ===
            if user.email:
                try:
                    message = (
                        f"Здравствуйте, {user.username}!\n\n"
                        "Вы успешно зарегистрировались на сайте DjangoCourse.\n"
                        "Теперь вы можете войти, используя ваш логин и пароль.\n\n"
                        "Если вы не регистрировались на этом сайте, просто проигнорируйте это письмо.\n\n"
                        "Это письмо отправлено автоматически, отвечать на него не нужно."
                    )

                    result = send_mail(
                        subject="Добро пожаловать в DjangoCourse!",
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )

                    print(f"Результат send_mail (register): {result}")
                except Exception as e:
                    print(f"❌ Ошибка отправки письма в register: {e}")
            # === конец блока отправки письма ===

            messages.success(request, "Вы успешно зарегистрировались! Теперь можно войти.")
            return redirect("login")

    else:
        form = SimpleRegisterForm()

    return render(request, "registration/register.html", {"form": form})


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


def custom_logout(request):
    logout(request)
    return redirect('login') 

def test_email(request):
    result = send_mail(
        subject="Тест от Django + Beget",
        message="Если ты видишь это письмо — SMTP точно работает 👍",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["andrej.zemskov.1987@bk.ru"],
        fail_silently=False,
    )
    print("Результат send_mail:", result)
    return HttpResponse("OK")
