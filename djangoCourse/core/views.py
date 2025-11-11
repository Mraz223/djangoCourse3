from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review

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
