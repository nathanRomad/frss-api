from django.db import models

class Questions(models.Model):
    text = models.CharField(max_length=255)
    explanation = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255)