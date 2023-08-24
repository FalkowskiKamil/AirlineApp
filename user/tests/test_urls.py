from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user.views import registration_request, login_request, logout_request

class TestUrls(SimpleTestCase):
    def test_registration_url_is_resolved(self):
        url = reverse("user:registration")
        self.assertEquals(resolve(url).func, registration_request)
        
    def test_login_url_is_resolved(self):
        url = reverse("user:login")
        self.assertEquals(resolve(url).func, login_request)

    def test_logout_url_is_resolved(self):
        url = reverse("user:logout")
        self.assertEquals(resolve(url).func, logout_request)