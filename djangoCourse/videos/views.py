from django.shortcuts import render, get_object_or_404
from .models import Video
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def video_list(request):
    videos = Video.objects.all().order_by('id')
    return render(request, 'videos/video_list.html', {'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'videos/video_detail.html', {'video': video})

@csrf_exempt
def video_list_api(request):
    if request.method == 'GET':
        videos = list(Video.objects.values('id', 'title', 'description', 'video_url'))
        return JsonResponse(videos, safe=False)