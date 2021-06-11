from django.db import models
from .questions import Questions

class Answers(models.Model):
    input_answer = models.IntegerField
    select_answer = models.CharField(max_length=255)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)