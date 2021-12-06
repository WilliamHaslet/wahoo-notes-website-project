from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Class, Profile, Assignment, Document
from .forms import UserUpdateForm, ProfileUpdateForm, DocumentForm

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
    def get_context_data(self, **kwargs):
        context = super(ClassDetailView, self).get_context_data(**kwargs)
        context['classdocs'] = Document.objects.filter(document_class=self.kwargs['pk'])
        return context

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
        if request.POST.get('assignment_name') and request.POST.get('class_name') and request.POST.get('description') and request.POST.get('due_date'):
            class_name = request.POST.get('class_name')
            name = request.POST.get('assignment_name')
            due_date = request.POST.get('due_date')
            description = request.POST.get('description')
            if len(class_name) > 30:
                messages.error(request, "Error: Class name must be less than or equal to 30 characters")
                return HttpResponseRedirect('/assignments')
            if len(name) > 30:
                messages.error(request, "Error: Assignment name must be less than or equal to 30 characters")
                return HttpResponseRedirect('/assignments')
            if len(due_date) > 30:
                messages.error(request, "Error: Due date must be less than or equal to 30 characters")
                return HttpResponseRedirect('/assignments')
            if len(description) > 200:
                messages.error(request, "Error: Description must be less than or equal to 200 characters")
                return HttpResponseRedirect('/assignments')
            new_assignment = Assignment()
            new_assignment.class_name = class_name
            new_assignment.name = name
            new_assignment.due_date = due_date
            new_assignment.description = description
            new_assignment.profile = request.user.profile
            new_assignment.save()
        else:
            messages.error(request, "Blank Submission! You must submit all fields.")
    return HttpResponseRedirect('/assignments')

def submitEditedProfile(request):
    if request.method == 'POST':
        if request.POST.get('studentName') or request.POST.get('studentComputingID') or request.POST.get('studentYear'):
            name = request.POST.get('studentName')
            computing_id = request.POST.get('studentComputingID')
            year = request.POST.get('studentYear')
            if len(name) > 30:
                messages.error(request, "Error: name must be less than or equal to 30 characters")
                return HttpResponseRedirect('/')
            if len(computing_id) > 30:
                messages.error(request, "Error: computing id must be less than or equal to 30 characters")
                return HttpResponseRedirect('/')
            if (not year.isdigit() or len(year) != 4) and year:
                messages.error(request, "Error: graduation year must be a 4 digit number")
                return HttpResponseRedirect('/')
            if name: request.user.profile.name = name
            if computing_id: request.user.profile.computing_id = computing_id
            if year: request.user.profile.year = year
            request.user.profile.save()
            messages.success(request, "Successfully Submitted!")
        else:
            messages.error(request, "Blank Submission!")
    return HttpResponseRedirect('/')

def filterClasses(request):
    template_name = 'main_app/filterclasses.html'
    courses = Class.objects
    if request.method == 'POST':
        searched = request.POST.get('query')
        searchType = request.POST.get('queryType')
        if searched == '': 
            messages.error(request, "Blank query!")
            return HttpResponseRedirect('/addClasses')
        if searchType =='':
            messages.error(request, "Blank filter!")
            return HttpResponseRedirect('/addClasses')
        elif searchType == 'name': courses = Class.objects.filter(name__icontains=searched)
        elif searchType == 'code':
            vals = searched.split(' ') # vals = [course subject, course code]
            # if len is not 2, course code is invalid
            if len(vals) != 2:
                messages.error(request, "Invalid course code!")
                return HttpResponseRedirect('/addClasses')
            # filter twice
            print("subject", vals[0], "\n")
            print("code", vals[1], "\n")
            courses = Class.objects.filter(subject__icontains=vals[0])
            courses = courses.filter(code__icontains=vals[1])
        elif searchType == 'professor': courses = Class.objects.filter(professor__icontains=searched)
        elif searchType == 'subject': courses = Class.objects.filter(subject__icontains=searched)
    return render(request, template_name, {'courses':courses, 'filter':searchType})

def addCourse(request, pk):
    if request.method == 'POST':
        course = Class.objects.get(id=pk)
        request.user.profile.classes.add(course)
        request.user.profile.save()
        messages.success(request, f"{course.subject} {course.code} added!")
    return HttpResponseRedirect(f'/course/{pk}/')

def removeCourse(request, pk):
    if request.method == 'POST':
        course = Class.objects.get(id=pk)
        request.user.profile.classes.remove(course)
        request.user.profile.save()
        messages.success(request, f"{course.subject} {course.code} removed!")
    return HttpResponseRedirect(f'/course/{pk}/')

def logout_view(request):
    logout(request)
    return render(request, 'main_app/index.html')

def studentSearchView(request):
    template = loader.get_template('main_app/studentSearch.html')

    otherStudents = []

    userProfile = request.user.profile
    #userProfile = Profile.objects.all()[0]

    for c in userProfile.classes.all():
        classData = {
            'students': [],
            'class': c
        }

        for student in c.profiles.all():
            if student != userProfile:
                classData['students'].append(student)

        otherStudents.append(classData)
    context = {
        'classes': otherStudents
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

    # Add all classes with class number below 8000 from json to database
    '''fallClasses = json.load(open("fallClasses.txt"))
    fallClassCount = len(fallClasses)

    for i in range(fallClassCount):
        if int(fallClasses[i][ClassData.catalogNumber][:30]) < 8000:
            newClass = Class.objects.create(id=fallClasses[i][ClassData.classNumber])
            newClass.subject = fallClasses[i][ClassData.subject][:30]
            newClass.code = fallClasses[i][ClassData.catalogNumber][:30]
            newClass.section = fallClasses[i][ClassData.classSection][:30]
            newClass.name = fallClasses[i][ClassData.classTitle][:30]
            newClass.professor = fallClasses[i][ClassData.instructor][:30]
            newClass.size = fallClasses[i][ClassData.enrollmentCapacity]
            newClass.day = fallClasses[i][ClassData.meetingDays][:30]
            newClass.start_time = fallClasses[i][ClassData.meetingTimeStart]
            newClass.end_time = fallClasses[i][ClassData.meetingTimeEnd]
            newClass.semester = fallClasses[i][ClassData.term][:30]
            newClass.save()'''
    return None

def document_list(request):
    userdocs = Document.objects.filter(profile=request.user.profile)
    return render(request, 'main_app/documents.html', {'documents': userdocs})

def document_upload(request):
    user = {'user': request.user}
    form = DocumentForm(**user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, **user)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.profile = request.user.profile
            doc.save()
            return HttpResponseRedirect('/documents')
    documents = Document.objects.all()
    return render(request, 'main_app/document_upload.html', {'documents': documents, 'form': form})

def document_delete(request, pk):
    if request.method == 'POST':
        form = Document.objects.get(pk=pk)
        form.document.delete()
        form.delete()
    documents = Document.objects.all()
    form = DocumentForm()
    return HttpResponseRedirect('/documents')
    #return render(request, 'main_app/documents.html', {'documents': documents, 'form': form})
