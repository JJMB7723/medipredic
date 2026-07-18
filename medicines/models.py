from django.db import models
from predictor.models import Disease

class Medicine(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='medicines')
    medicine_name = models.CharField(max_length=255)
    dosage = models.TextField(help_text="Standard dosage information")
    side_effects = models.TextField(help_text="Common side effects")
    warnings = models.TextField(help_text="Contraindications and emergency warnings")

    def __str__(self):
        return f"{self.medicine_name} (for {self.disease.name})"
