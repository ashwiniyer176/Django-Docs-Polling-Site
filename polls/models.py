from django.db import models
import datetime
from django.utils import timezone
# Create your models here.


class Question(models.Model):
    questionText = models.CharField(max_length=200)
    publishedDate = models.DateTimeField('date published')

    def __str__(self):
        return self.questionText

    def wasPublishedRecently(self):
        now = timezone.now()
        return now-datetime.timedelta(days=1) <= self.publishedDate <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choiceText = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choiceText


class Author(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    authorName = models.CharField(max_length=100)

    def __str__(self):
        return self.authorName
