from django.db import models

class Questions(models.Model):
    text = models.CharField(max_length=255)