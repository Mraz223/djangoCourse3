from .models import Achievement

def give_first_solve_achievement(user):
    achievement, _ = Achievement.objects.get_or_create(
        title='Первое решение',
        defaults={'description': 'Ты решил(а) свою первую задачу!'}
    )
    if user not in achievement.users.all():
        achievement.users.add(user)
