from django.db import models


class AnalysisResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    job_title = models.CharField(max_length=255, blank=True)
    match_score = models.IntegerField(default=0)
    matched_skills = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    summary = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Analysis #{self.id} — {self.match_score}% match ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
