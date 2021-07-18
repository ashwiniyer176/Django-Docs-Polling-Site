from django import template
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import context, loader
from django.urls import reverse
# Create your views here.
from .models import Question, Choice


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
    question = get_object_or_404(Question, pk=questionID)
    return render(request, 'polls/results.html', context={'question': question})


def vote(request, questionID):
    question = get_object_or_404(Question, pk=questionID)
    try:
        selectedChoice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', context={
            'question': question,
            'error': "You did not select a choice"
        })
    else:
        selectedChoice.votes += 1
        selectedChoice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
