from django.db import models
from django.contrib.auth.models import User
from .questions import Questions
from .options import Options

class Answers(models.Model):
    input_answer = models.IntegerField()
    option_id = models.ForeignKey(Options, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)