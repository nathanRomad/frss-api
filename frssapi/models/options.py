from frssapi.models.questions import Questions
from django.db import models

class Options(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    point_value = models.IntegerField()