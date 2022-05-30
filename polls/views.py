
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('pub_date')[:5]

class PaperView(generic.ListView):
    template_name = 'polls/paper.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
class PaperResultsView(generic.ListView):
    template_name = 'polls/presults.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('pub_date')
    
class MainView(generic.ListView):
    template_name = 'polls/main.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('pub_date')[:5]
    
def vote(request):
    n = 0
    for p in Choice.objects.all():
        p.votes = False
        p.save()
    for i in Question.objects.order_by('pub_date'):
        n+=1
        question = i
        try:
            selected_choice = question.choice_set.get(pk=request.POST[f'choice_{n}'])
            selected_choice.votes = True
            selected_choice.recent += 1
            selected_choice.save()
        except (KeyError, Choice.DoesNotExist):
            pass
            # Redisplay the question voting form.
            # return render(request, 'polls/detail.html', {
            #     'question': question,
            #     'error_message': "You didn't select a choice.",
            # })
        # else:
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
        # return HttpResponseRedirect(reverse('polls:presults', args=(question.id,)))
    return HttpResponseRedirect(reverse('polls:presults'))

def reset(request):
    for choice in Choice.objects.all():
        choice.recent = 0
        choice.votes = False
        choice.save()
    return HttpResponseRedirect(reverse('polls:main'))