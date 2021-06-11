from frssapi.models.questions import Questions
from django.db import models

class Options(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)