from django.shortcuts import render, get_object_or_404
from .models import Task
from users.utils import give_first_solve_achievement
from .utils import get_daily_task
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user_code = ""
    result = None

    if request.method == "POST":
        user_code = request.POST.get("code", "")
        input_data = task.input_data
        expected_output = task.expected_output

        import io
        import sys

        old_stdout = sys.stdout
        old_stdin = sys.stdin
        sys.stdout = buffer = io.StringIO()
        sys.stdin = io.StringIO(input_data)

        try:
            exec(user_code, {})
            output = buffer.getvalue().strip()
            result = (output == expected_output.strip())
            if result:
                give_first_solve_achievement(request.user)
        except Exception as e:
            output = str(e)
            result = False
        finally:
            sys.stdout = old_stdout
            sys.stdin = old_stdin

        return render(request, "tasks/task_detail.html", {
            "task": task,
            "user_code": "",
            "output": output,
            "is_correct": result
        })

    return render(request, "tasks/task_detail.html", {"task": task})


def task_list(request):
    tasks = Task.objects.all()
    
   
    paginator = Paginator(tasks, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tasks/task_list.html', {'page_obj': page_obj})


def daily_task(request):
    task = get_daily_task()
    if not task:
        return render(request, "tasks/no_daily_task.html")  
    return render(request, "tasks/task_detail.html", {"task": task})

@csrf_exempt
def task_list_api(request):
    if request.method == 'GET':
        tasks = list(Task.objects.values(
            'id', 
            'title', 
            'description',
            'input_data', 
            'expected_output'
        ))
        return JsonResponse(tasks, safe=False)


@csrf_exempt
def check_solution_api(request, task_id):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            print("Raw body:", body)
            
            if not body:
                return JsonResponse({'status': 'error', 'message': 'Empty body'})
            
            data = json.loads(body)
            user_code = data.get('code', '').strip()
            
            if not user_code:
                return JsonResponse({'status': 'error', 'message': 'Код не предоставлен'})
            
            task = Task.objects.get(id=task_id)
            
            return JsonResponse({
                'status': 'success', 
                'correct': True,
                'message': f'Решение для "{task.title}" принято!'
            })
            
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': f'JSON error: {str(e)}'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Задача не найдена'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'})