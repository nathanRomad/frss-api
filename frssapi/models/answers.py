from django.db import models
from django.contrib.auth.models import User
from .questions import Questions
from .options import Options


class Answers(models.Model):
    input_answer = models.IntegerField(null=True)
    option = models.ForeignKey(Options, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("question", "user")