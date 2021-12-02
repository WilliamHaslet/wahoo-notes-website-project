# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from django.http import HttpRequest
# from django.template.loader import render_to_string

# from main_app.models import Class, Assignment
# from main_app.forms import ProfileUpdateForm
# from main_app.views import ListClassesView

# #Login and logout
# class LoginTest(TestCase):
#     #Correctly Setup User
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create(username='user')
#         user.set_password('password')
#         user.save()

#     def test_login(self):
#         c = Client()
#         logged_in = c.login(username='user', password='password')
#         self.assertTrue(logged_in)

# class LogoutTest(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create(username='user1')
#         user.set_password('password')
#         user.save()

#     def test_logout(self):
#         c = Client()
#         c.login(username='user1', password='password')
#         User = get_user_model()
#         user = User.objects.get(username='user1')
#         self.assertTrue (user.is_authenticated)
#         c.logout()
#         self.assertFalse(user.is_anonymous)

# #Classes
# import json
# from enum import IntEnum

# class ClassData(IntEnum):
#     subject = 0
#     catalogNumber = 1
#     classSection = 2
#     classNumber = 3
#     classTitle = 4
#     classTopicFormalDesc = 5
#     instructor = 6
#     enrollmentCapacity = 7
#     meetingDays = 8
#     meetingTimeStart = 9
#     meetingTimeEnd = 10
#     term = 11
#     year = 12

# def createClass(i):
#     # arguement i is the index of the class in the fallClass.txt json file
#     fallClasses = json.load(open("fallClasses.txt"))
#     fallClassCount = len(fallClasses)

#     newClass = Class.objects.create(id=fallClasses[i][ClassData.classNumber])
#     newClass.subject = fallClasses[i][ClassData.subject][:30]
#     newClass.code = fallClasses[i][ClassData.catalogNumber][:30]
#     newClass.section = fallClasses[i][ClassData.classSection][:30]
#     newClass.name = fallClasses[i][ClassData.classTitle][:30]
#     newClass.professor = fallClasses[i][ClassData.instructor][:30]
#     newClass.size = fallClasses[i][ClassData.enrollmentCapacity]
#     newClass.day = fallClasses[i][ClassData.meetingDays][:30]
#     newClass.start_time = fallClasses[i][ClassData.meetingTimeStart]
#     newClass.end_time = fallClasses[i][ClassData.meetingTimeEnd]
#     newClass.semester = fallClasses[i][ClassData.term][:30]
#     newClass.save()
#     return newClass

# class AddClassTest(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create(username='user1')
#         user.set_password('password')
#         user.save()

#     def test_addclass(self):
#         User = get_user_model()
#         testUser = User.objects.get(username='user1')
        
#         course = createClass(3000)
        
#         testUser.profile.classes.add(course)
#         testUser.profile.save()
        
#         c = testUser.profile.classes.get(id=course.id)
#         self.assertTrue(c.name == course.name)
#         self.assertTrue(Class.objects.get(name=course.name) == c)

# class RemoveClassTest2(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create(username='user1')
#         user.set_password('password')
#         user.save()

#     def test_addclass(self):
#         User = get_user_model()
#         testUser = User.objects.get(username='user1')
        
#         course = createClass(3000)
        
#         testUser.profile.classes.add(course)
#         testUser.profile.save()

#         c = testUser.profile.classes.get(id=course.id)
#         self.assertTrue(c.name == course.name)
#         self.assertTrue(Class.objects.get(name=course.name) == c)

#         testUser.profile.classes.remove(course)

#         c = testUser.profile.classes.filter(id=course.id)
#         self.assertTrue(len(c) == 0)
        
# class RemoveClassTest(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create(username='user1')
#         user.set_password('password')
#         user.save()

#     def test_removeclass(self):
#         User = get_user_model()
#         testUser = User.objects.get(username='user1')
        
#         course = createClass(3000)
        
#         testUser.profile.classes.add(course)
#         testUser.profile.save()

#         testUser.profile.classes.remove(course)
#         testUser.profile.save()
#         self.assertFalse(testUser.profile.classes.exists())

# #Assignments
# def createAssignment(profile):
#     newAssign = Assignment()
#     newAssign.id = 0
#     newAssign.profile = profile
#     newAssign.name = "Test Assignment"
#     newAssign.description = "Just a test"
#     newAssign.points = 100
#     newAssign.class_name = "CS3240"
#     newAssign.release_date = "11/1/21"
#     newAssign.due_date = "1/19/38"
#     newAssign.save()
#     return newAssign

# class AddAssignmentTest(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create(username='user1')
#         user.set_password('password')
#         user.save()

#     def test_addassignment(self):
#         User = get_user_model()
#         testUser = User.objects.get(username='user1')
#         assignment = createAssignment(testUser.profile)
#         assignment.save()
        
#         a = Assignment.objects.get(id=assignment.id)
#         self.assertTrue(a.profile == assignment.profile)
#         self.assertTrue(a.name == assignment.name)
#         self.assertTrue(a.description == assignment.description)
#         self.assertTrue(a.class_name == assignment.class_name)
#         self.assertTrue(a.due_date == assignment.due_date)

# class RemoveAssignmentTest(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create(username='user1')
#         user.set_password('password')
#         user.save()

#     def test_removeassignment(self):
#         User = get_user_model()
#         testUser = User.objects.get(username='user1')
#         assignment = createAssignment(testUser.profile)
#         assignment.save()
#         assigntest = Assignment.objects.get(id=assignment.id)
#         assigntest.delete()
#         self.assertFalse(Assignment.objects.exists())

# #Profile
# class EditProfileTest(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create(username='user1')
#         user.set_password('password')
#         user.save()

#     def test_editprofile(self):
#         User = get_user_model()
#         testUser = User.objects.get(username='user1')
#         request = HttpRequest()
#         request.POST = {
#             "computing_id": "tes7er",
#             "year": 2021,
#         }

#         form = ProfileUpdateForm(request.POST, instance=testUser.profile)
#         form.save()
#         self.assertTrue(testUser.profile.computing_id == "tes7er")
#         self.assertTrue(testUser.profile.year == 2021)
