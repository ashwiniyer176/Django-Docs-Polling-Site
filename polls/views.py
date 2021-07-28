from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
# Create your views here.
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questionsList'

    def get_queryset(self):
        '''Return the last five published questions'''
        return Question.objects.order_by('-publishedDate')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


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
