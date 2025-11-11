import random
from datetime import date
from .models import Task

def get_daily_task():
    today = date.today().isoformat()  
    tasks = Task.objects.filter(is_daily_candidate=True).order_by('id')
    if not tasks.exists():
        return None

    
    index = hash(today) % tasks.count()
    return tasks[index]
