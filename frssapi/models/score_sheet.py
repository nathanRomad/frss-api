from django.db import models
from django.contrib.auth.models import User
from .questions import Questions

class ScoreSheet(models.Model):
    answer = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)