from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, UVAClass, Student
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('editstudent')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main_app/editstudent.html')

class IndexView(generic.ListView):
    model = Student
    template_name = 'main_app/index.html'
    context_object_name = 'profile'


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

class StudentView(generic.ListView):
    model = Student
    template_name = 'main_app/editprofile.html'

class EditStudentView(generic.ListView):
    model = Student
    template_name = 'main_app/editstudent.html'
    context_object_name = 'profile'

class UVAClassListView(generic.ListView):
    model = UVAClass
    template_name = 'main_app/list.html'
    context_object_name = 'curr_classes'
    def get_queryset(self):
        """
        Filters classes by user
        """
        return UVAClass.objects.filter(user=self.request.user)

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

def addClass(request):
    if request.method=='POST':
        if request.POST.get('uvaclass_id') and request.POST.get('uvaclass_yr'):
            new_class = UVAClass()
            new_class.user = request.user
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

def submitEditedStudent(request):
    if request.method=='POST':
        if request.POST.get('studentComputingID') and request.POST.get('studentYear'):
            request.user.profile.computing_id=request.POST.get('studentComputingID')
            request.user.profile.year=request.POST.get('studentYear')
            request.user.profile.save()
            messages.success(request, "Successfully Submitted!")
        else:
            messages.error(request, "Blank Submission! You must submit all fields.")
    return render(request, 'main_app/editstudent.html')

def logout_view(request):
    logout(request)
    return render(request, 'main_app/index.html')