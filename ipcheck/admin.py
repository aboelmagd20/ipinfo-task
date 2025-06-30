from django.contrib import admin
from .models import IPInfo
from django_celery_results.models import TaskResult



@admin.register(IPInfo)
class IPInfoAdmin(admin.ModelAdmin):
    list_display = ('ip', 'country', 'city', 'org', 'submitted_by', 'processed', 'created_at')
    list_filter = ('submitted_by', 'processed', 'country', 'region', 'city')
    search_fields = ('ip', 'country', 'region', 'city', 'org', 'submitted_by__username')
    ordering = ('-created_at',)