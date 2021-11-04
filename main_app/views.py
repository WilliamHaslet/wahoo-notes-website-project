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

from django.http import HttpResponse
import requests
import json
from pprint import pprint
from enum import IntEnum
from django.template import loader

class ClassData(IntEnum):
    subject = 0
    catalogNumber = 1
    classSection = 2
    classNumber = 3
    classTitle = 4
    classTopicFormalDesc = 5
    instructor = 6
    enrollmentCapacity = 7
    meetingDays = 8
    meetingTimeStart = 9
    meetingTimeEnd = 10
    term = 11
    year = 12

def classTestView(request):
    fallClasses = json.load(open("fallClasses.txt"))

    fallClassCount = len(fallClasses)
    subjects = []
    numbers = []
    professors = []
    startTimes = []

    for i in range(fallClassCount):
        subject = fallClasses[i][ClassData.subject]
        if not subject in subjects:
            subjects.append(subject)
            
        number = fallClasses[i][ClassData.catalogNumber]
        if not number in numbers:
            numbers.append(number)

        professor = fallClasses[i][ClassData.instructor]
        if (not professor in professors) and professor != "":
            professors.append(professor)

        startTime = fallClasses[i][ClassData.meetingTimeStart]
        if not startTime in startTimes:
            startTimes.append(startTime)

    template = loader.get_template('main_app/classTest.html')
    context = {
        'displayData': [
            ("Subject", subjects),
            ("Class Number", numbers),
            ("Professor", professors),
            ("Start Time", startTimes)
        ]
    }

    return HttpResponse(template.render(context, request))
