from django.test import TestCase, Client
from django.contrib.auth import get_user_model

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
            