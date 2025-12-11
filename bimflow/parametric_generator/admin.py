from django.contrib import admin
from .models import GeneratedModel, GenerationTask

@admin.register(GeneratedModel)
class GeneratedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'program_spec', 'asset_type', 'status', 'created_at']
    list_filter = ['asset_type', 'status']

@admin.register(GenerationTask)
class GenerationTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'task_id', 'status']