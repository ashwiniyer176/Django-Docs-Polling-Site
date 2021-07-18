from django import template
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import context, loader
# Create your views here.
from .models import Question


def index(request):
    questionsList = Question.objects.order_by('-publishedDate')[:5]
    context = {
        'questionsList': questionsList
    }
    return render(request, 'polls/index.html', context)


def detail(request, questionID):
    try:
        question = Question.objects.get(pk=questionID)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


def results(request, questionID):
    response = "You're looking at results of question %s"
    return HttpResponse(response % questionID)


def vote(request, questionID):
    return HttpResponse("You're voting on question %s." % questionID)
