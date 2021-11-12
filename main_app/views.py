from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Class, Profile, Assignment
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
    context_object_name = 'index'

class EditProfileView(generic.ListView):
    model = Profile
    template_name = 'main_app/editprofile.html'
    context_object_name = 'profile'

class AddClassesView(generic.ListView):
    model = Class
    template_name = 'main_app/addclasses.html'
    context_object_name = 'all_classes'
    courses = []

class ListClassesView(generic.ListView):
    model = Profile
    template_name = 'main_app/listclasses.html'
    context_object_name = 'my_classes'
    def get_queryset(self):
        return Class.objects.order_by('id')
    def get_context_data(self, **kwargs):
        context = super(ListClassesView, self).get_context_data(**kwargs)
        context['Mon'] = self.request.user.profile.classes.filter(day__icontains="M").order_by('start_time')
        context['Tue'] = self.request.user.profile.classes.filter(day__icontains="T").order_by('start_time')
        context['Wed'] = self.request.user.profile.classes.filter(day__icontains="W").order_by('start_time')
        context['Thu'] = self.request.user.profile.classes.filter(day__icontains="R").order_by('start_time')
        context['Fri'] = self.request.user.profile.classes.filter(day__icontains="F").order_by('start_time')
        return context

class ClassDetailView(generic.DetailView):
    model = Class
    template_name = 'main_app/classdetail.html'
    context_object_name = 'class_detail'

class AssignmentsView(generic.ListView):
    template_name = 'main_app/assignments.html'
    context_object_name = 'my_assignments'
    def get_queryset(self):
        return self.request.user.profile.assignments.all()

def removeAssignment(request, pk):
    if request.method == 'POST':
        assignment = Assignment.objects.get(id=pk)
        assignment.delete()
    return HttpResponseRedirect('/assignments')

def addAssignment(request):
    template_name = 'main_app/filterclasses.html'
    if request.method == 'POST':
        new_assignment = Assignment()
        new_assignment.name = request.POST.get('assignment_name')
        new_assignment.class_name = request.POST.get('class_name')
        new_assignment.description = request.POST.get('description')
        new_assignment.save()
        request.user.profile.assignments.add(new_assignment)
        request.user.profile.save()
    return HttpResponseRedirect('/assignments')

def submitEditedProfile(request):
    if request.method == 'POST':
        if request.POST.get('studentComputingID') and request.POST.get('studentYear'):
            request.user.profile.computing_id=request.POST.get('studentComputingID')
            request.user.profile.year=request.POST.get('studentYear')
            request.user.profile.save()
            messages.success(request, "Successfully Submitted!")
        else:
            messages.error(request, "Blank Submission! You must submit all fields.")
    return HttpResponseRedirect('/editprofile')

def filterClasses(request):
    template_name = 'main_app/filterclasses.html'
    courses = Class.objects
    if request.method == 'POST':
        searched = request.POST.get('query')
        searchType = request.POST.get('queryType')
        if searched == '': 
            messages.error(request, "Blank query!")
            return HttpResponseRedirect('/addClasses')
        elif searchType == 'name': courses = Class.objects.filter(name__icontains=searched)
        elif searchType == 'id': courses = Class.objects.filter(id__icontains=searched)
        elif searchType == 'professor': courses = Class.objects.filter(professor__icontains=searched)
        elif searchType == 'subject': courses = Class.objects.filter(subject__icontains=searched)
    return render(request, template_name, {'courses':courses})

def addCourse(request, pk):
    if request.method == 'POST':
        course = Class.objects.get(id=pk)
        request.user.profile.classes.add(course)
        request.user.profile.save()
        messages.success(request, f"{course.subject} {course.code} added!")
    return HttpResponseRedirect('/addClasses')

def removeCourse(request, pk):
    if request.method == 'POST':
        course = Class.objects.get(id=pk)
        request.user.profile.classes.remove(course)
        request.user.profile.save()
        messages.success(request, f"{course.subject} {course.code} removed!")
    return HttpResponseRedirect('/addClasses')

def logout_view(request):
    logout(request)
    return render(request, 'main_app/index.html')

def studentSearchView(request):
    template = loader.get_template('main_app/studentSearch.html')

    otherStudents = []

    for c in request.user.profile.classes.all():
        for stu in c.profiles.all():
            if stu == request.user.profile:
                continue
            exists = False
            for o in otherStudents:
                if o['student'] == stu:
                    exists = True
                    break
            if not exists:
                otherStudents.append({
                    'student': stu,
                    'sharedClasses': []
                })
            for o in otherStudents:
                if o['student'] == stu:
                    o['sharedClasses'].append(c)
                    break

    context = {
        'students': otherStudents
    }
    return HttpResponse(template.render(context, request))

def classesDebugView(request):
    template = loader.get_template('main_app/classesDebug.html')
    context = {
        'classCount': len(Class.objects.all()),
        'allClasses': Class.objects.all()
    }
    return HttpResponse(template.render(context, request))

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
    # Delete all classes with class number above 8000
    '''fallClasses = json.load(open("fallClasses.txt"))
    fallClassCount = len(fallClasses)

    for i in range(fallClassCount):
        newClass = Class.objects.get(id=fallClasses[i][ClassData.classNumber])
        if int(newClass.code) >= 8000:
            newClass.delete()'''
    return None
