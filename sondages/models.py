from django.db import models
from django.utils import timezone
from datetime import timedelta


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
