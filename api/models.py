from django.db import models
from django.contrib.auth.models import User


class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    total_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Question(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"Score: {self.score}"