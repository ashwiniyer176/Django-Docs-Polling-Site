from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

import datetime
from .models import Question
# Create your tests here


def createQuestion(questionText, days):
    time = timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(questionText=questionText, publishedDate=time)


class QuestionModelTests(TestCase):
    def testWasPublishedRecently_InFuture(self):
        """
        wasPublishedRecently() returns False for questions whose publishedDate is in the future
        """
        time = timezone.now()+datetime.timedelta(days=30)
        future_question = Question(publishedDate=time)
        self.assertIs(future_question.wasPublishedRecently(), False)


class QuestionIndexViewTests(TestCase):
    def testNoQuestions(self):
        """
        If no questions exist, appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['questionsList'], [])

    def testPastQuestion(self):
        """
        Questions with publishedDate in the past are displayed on the index page
        """
        question = createQuestion("Past Question", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['questionsList'], [question])

    def testFutureQuestion(self):
        """
        Questions with publishedDate in the future are not displayed
        """
        question = createQuestion("Future", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['questionsList'], [])

    def testFutureAndPastQuestion(self):
        past = createQuestion("Past", days=-17)
        future = createQuestion("Future", days=15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['questionsList'], [past])

    def test2PastQuestions(self):
        q1 = createQuestion("P1", days=-10)
        q2 = createQuestion("P2", days=-20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['questionsList'], [q1, q2])
