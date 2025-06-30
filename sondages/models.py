from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=250)
    pub_date  = models.DateTimeField()

    def recent_question(self):
        return self.pub_date >= timezone.now() - timedelta(days=1)

    def __str__(self):
        return self.question_text

class Choix(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choix_text = models.CharField(max_length=250)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choix_text
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choix = models.ForeignKey(Choix, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)





