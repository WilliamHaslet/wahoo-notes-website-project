from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Class, Profile
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
            return redirect('editprofile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main_app/editprofile.html')

class IndexView(generic.ListView):
    model = Profile
    template_name = 'main_app/index.html'
    context_object_name = 'profile'

class EditProfileView(generic.ListView):
    model = Profile
    template_name = 'main_app/editprofile.html'
    context_object_name = 'profile'

class AddClassesView(generic.ListView):
    model = Class
    template_name = 'main_app/addclasses.html'
    context_object_name = 'all_classes'

class ListClassesView(generic.ListView):
    model = Profile
    template_name = 'main_app/listclasses.html'
    context_object_name = 'my_classes'

def submitEditedProfile(request):
    if request.method=='POST':
        if request.POST.get('studentComputingID') and request.POST.get('studentYear'):
            request.user.profile.computing_id=request.POST.get('studentComputingID')
            request.user.profile.year=request.POST.get('studentYear')
            request.user.profile.save()
            messages.success(request, "Successfully Submitted!")
        else:
            messages.error(request, "Blank Submission! You must submit all fields.")
    return render(request, 'main_app/editprofile.html')

def logout_view(request):
    logout(request)
    return render(request, 'main_app/index.html')