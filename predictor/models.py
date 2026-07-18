from django.db import models

class Disease(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(help_text="Detailed description of the disease")
    causes = models.TextField(help_text="Primary causes of the disease")
    precautions = models.TextField(help_text="Comma-separated precautions or guidelines")
    specialist = models.CharField(max_length=255, help_text="Specialist medical field suggested")

    def __str__(self):
        return self.name

    def get_precautions_list(self):
        """Returns precautions as a list"""
        if not self.precautions:
            return []
        return [p.strip() for p in self.precautions.split(',') if p.strip()]
