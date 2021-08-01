from .forms import QuestionForm
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questionsList'

    def get_queryset(self):
        '''Return the last five published questions'''
        return Question.objects.filter(
            publishedDate__lte=timezone.now()
        ).order_by('-publishedDate')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(publishedDate__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# TODO: create choices for question created via form
# TODO: write test to ensure no question has zero choices


def createQuestion(request):
    if(request.method == "POST"):
        form = QuestionForm(request.POST)
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('polls:index'))
    else:
        form = QuestionForm()
        return render(request, 'polls/question.html', {'form': form})


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
