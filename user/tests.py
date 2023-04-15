from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
import unittest

# Create your tests here.

class UserTest(TestCase):
    def setup(self):
        self.client = Client()
        self.user = User.objects.create_user(
                username = 'testuser',
                password = 'testpass'
            )
        
    def test_login_url(self):
        response = self.client.get('/user/login/')
        self.failUnlessEqual(response.status_code, 200)
    
    def test_registration_url(self):
        response = self.client.get('/user/registration/')
        self.failUnlessEqual(response.status_code, 200)
        
    def test_logout_url(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user:logout'))
        self.assertRedirects(response, reverse('onlinecourse:index'))
        self.assertFalse('_auth_user_id' in self.client.session)

if __name__=='__main__':
	unittest.main()