from django.contrib import admin
from .models import AnalysisResult

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'match_score', 'created_at')
    readonly_fields = ('created_at',)
