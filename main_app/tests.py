from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from main_app.models import Class

class LoginTest(TestCase):

    #Correctly Setup User
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='user')
        user.set_password('password')
        user.save()

    def test_login(self):
        c = Client()
        logged_in = c.login(username='user', password='password')
        self.assertTrue(logged_in)

class LogoutTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='user1')
        user.set_password('password')
        user.save()

    def test_logout(self):
        c = Client()
        c.login(username='user1', password='password')
        User = get_user_model()
        user = User.objects.get(username='user1')
        self.assertTrue (user.is_authenticated)
        c.logout()
        self.assertFalse(user.is_anonymous)

import json
from enum import IntEnum

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

def createClass(i):
    # arguement i is the index of the class in the fallClass.txt json file
    fallClasses = json.load(open("fallClasses.txt"))
    fallClassCount = len(fallClasses)

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
    newClass.save()
    return newClass

class AddClassTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='user1')
        user.set_password('password')
        user.save()

    def test_addclass(self):
        User = get_user_model()
        testUser = User.objects.get(username='user1')
        
        course = createClass(3000)
        
        testUser.profile.classes.add(course)
        testUser.profile.save()
        
        c = testUser.profile.classes.get(id=course.id)
        self.assertTrue(c.name == course.name)
        self.assertTrue(Class.objects.get(name=course.name) == c)

class RemoveClassTest2(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='user1')
        user.set_password('password')
        user.save()

    def test_addclass(self):
        User = get_user_model()
        testUser = User.objects.get(username='user1')
        
        course = createClass(3000)
        
        testUser.profile.classes.add(course)
        testUser.profile.save()
        
        c = testUser.profile.classes.get(id=course.id)
        self.assertTrue(c.name == course.name)
        self.assertTrue(Class.objects.get(name=course.name) == c)

        testUser.profile.classes.remove(course)

        c = testUser.profile.classes.filter(id=course.id)
        self.assertTrue(len(c) == 0)


