from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout

from .forms import DocumentForm
from .models import Choice, Question, UVAClass, Document



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

class UVAClassView(generic.ListView):
    model = UVAClass
    template_name = 'main_app/uvaclass.html'

class UVAClassListView(generic.ListView):
    model = UVAClass
    template_name = 'main_app/list.html'
    context_object_name = 'curr_classes'
    def get_classes(self):
        """
        Return all classes.
        """
        return UVAClass

    #Django upload files
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #for property, value in vars(form).items():
             #   print(property, ":", value)
            return HttpResponseRedirect('/documents')
    else:
        form = DocumentForm()
    documents = Document.objects.all()
    return render(request, 'main_app/documents.html', {'documents': documents, 'form': form})

def document_delete(request, pk):
    if request.method == 'POST':
        form = Document.objects.get(pk=pk)
        form.delete()
    return render(request, 'main_app/documents.html')


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
        if request.POST.get('uvaclass_id') and request.POST.get('uvaclass_yr'):
            new_class = UVAClass()
            new_class.id_text=request.POST.get('uvaclass_id')
            new_class.studentyr_text=request.POST.get('uvaclass_yr')
            new_class.classname_text=request.POST.get('uvaclass_cc')
            new_class.classtime_text=request.POST.get('uvaclass_time')
            new_class.classinst_text=request.POST.get('uvaclass_inst')
            new_class.save()
            messages.success(request, "Successfully Submitted!")
        else:
            messages.error(request, "Blank Submission! You must fill out the entire form.")
    return render(request, 'main_app/uvaclass.html')

def logout_view(request):
    logout(request)
    return render(request, 'main_app/index.html')