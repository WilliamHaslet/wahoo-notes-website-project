from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from main_app.models import UVAClass

class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
    
    def test_dummy_test_case(self):
        self.assertEqual(1, 1)

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

class AddClassTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username='user1')
        user.set_password('password')
        user.save()

    def test_addclass(self):
        User = get_user_model()
        user = User.objects.get(username='user1')
        UVAClass.objects.create(user=user, id_text="tes7er", studentyr_text="2023", classname_text="CS3240", classtime_text="11:00AM", classinst_text="Sherriff" )
        classentry = UVAClass.objects.get(user=user)
        classentry_str = classentry.user.username + " " + classentry.id_text + " " + classentry.studentyr_text + " " + classentry.classname_text + " " + classentry.classtime_text + " " + classentry.classinst_text
        self.assertEquals(classentry_str,"user1 tes7er 2023 CS3240 11:00AM Sherriff")
