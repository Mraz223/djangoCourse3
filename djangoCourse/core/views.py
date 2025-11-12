from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review
from django.contrib.auth.models import User
from django.http import HttpResponse

@login_required
def video_list_view(request):
    return render(request, 'courses/video_list.html')


@login_required
def reviews_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                user=request.user,
                text=form.cleaned_data['text'],
            )
            return redirect('reviews')  # имя url-ссылки ниже
    else:
        form = ReviewForm()

    reviews = Review.objects.select_related('user').all()

    context = {
        'form': form,
        'reviews': reviews,
    }
    return render(request, 'reviews/review_list.html', context)


def create_admin(request):
    """
    Временный маршрут для создания суперпользователя без консоли.
    После успешного создания удали этот код!
    """
    if User.objects.filter(username='admin').exists():
        return HttpResponse("⚠️ Админ уже существует.")
    else:
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        return HttpResponse("✅ Суперпользователь создан! Логин: admin / Пароль: admin123")
