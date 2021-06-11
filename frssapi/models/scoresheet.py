from django.db import models
from django.contrib.auth.models import User
from .answers import Answers

class ScoreSheet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(Answers, on_delete=models.CASCADE)