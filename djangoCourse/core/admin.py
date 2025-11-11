from .models import Review
from django.contrib import admin


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at',)
