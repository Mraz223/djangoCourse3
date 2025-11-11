from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    input_data = models.TextField(blank=True)
    expected_output = models.TextField()
    is_daily_candidate = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.title
