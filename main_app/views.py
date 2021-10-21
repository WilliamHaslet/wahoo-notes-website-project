from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question, Deepthought


class IndexView(generic.ListView):
    template_name = 'main_app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'main_app/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'main_app/results.html'

class DeepthoughtView(generic.ListView):
    model = Deepthought
    template_name = 'main_app/deepthoughts.html'

class DeepthoughtListView(generic.ListView):
    model = Deepthought
    template_name = 'main_app/list.html'
    context_object_name = 'curr_thoughts'
    def get_thoughts(self):
        """
        Return all thoughts.
        """
        return Deepthought

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'main_app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('main_app:results', args=(question.id,)))

def express(request):
    if request.method=='POST':
        if request.POST.get('deepthoughts') and request.POST.get('deepthoughts_title'):
            new_thought = Deepthought()
            new_thought.thought_text=request.POST.get('deepthoughts')
            new_thought.title_text=request.POST.get('deepthoughts_title')
            new_thought.save()
            messages.success(request, "Successfully Submitted!")
        else:
            messages.error(request, "Blank Submission! You must submit both a title and thought.")
    return render(request, 'main_app/deepthoughts.html')