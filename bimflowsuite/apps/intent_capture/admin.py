from django.contrib import admin
from django.utils.html import format_html
from .models import IntentCapture, ProgramSpec
import json

@admin.register(IntentCapture)
class IntentCaptureAdmin(admin.ModelAdmin):
    list_display = ['user', 'intent_text_preview', 'status', 'use_local_ml', 'created_at']
    list_filter = ['status', 'use_local_ml', 'created_at', 'user']
    search_fields = ['intent_text', 'user__username']
    readonly_fields = ['error_message', 'created_at']

    def intent_text_preview(self, obj):
        return obj.intent_text[:50] + "..." if len(obj.intent_text) > 50 else obj.intent_text
    intent_text_preview.short_description = 'Intent Text Preview'

    actions = ['process_selected_intents']

    def process_selected_intents(self, request, queryset):
        updated = 0
        for intent in queryset.filter(status='pending'):
            spec_data = {"floors": 3, "dimensions": "20x15"}
            ProgramSpec.objects.create(intent=intent, json_spec=spec_data)
            intent.status = 'processed'
            intent.save()
            updated += 1
        self.message_user(request, f'Processed {updated} intents.')
    process_selected_intents.short_description = "Process selected pending intents"

@admin.register(ProgramSpec)
class ProgramSpecAdmin(admin.ModelAdmin):
    list_display = ['intent', 'json_spec_preview', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['json_spec_formatted', 'created_at']

    def json_spec_preview(self, obj):
        return str(obj.json_spec)[:100] + "..." if obj.json_spec else "{}"
    json_spec_preview.short_description = 'JSON Spec Preview'

    def json_spec_formatted(self, obj):
        return format_html('<pre>{}</pre>', json.dumps(obj.json_spec, indent=2))
    json_spec_formatted.short_description = 'JSON Spec (Formatted)'