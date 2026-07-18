from django.db import models
from django.contrib.auth.models import User

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    symptoms = models.TextField(help_text="Comma-separated symptoms selected")
    predicted_disease = models.CharField(max_length=255, help_text="Predicted disease name")
    confidence_score = models.FloatField(default=0.0, help_text="Percentage confidence score")
    medicines = models.TextField(blank=True, help_text="Comma-separated list of recommended medications")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.predicted_disease} on {self.created_at.strftime('%Y-%m-%d')}"

    def get_symptoms_list(self):
        """Returns symptoms as a list of readable names"""
        if not self.symptoms:
            return []
        return [s.replace('_', ' ').strip().capitalize() for s in self.symptoms.split(',') if s.strip()]

    def get_medicines_list(self):
        """Returns medicines as a list"""
        if not self.medicines:
            return []
        return [m.strip() for m in self.medicines.split(',') if m.strip()]
