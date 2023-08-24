from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
import random
import string


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = self.random_register_data()
        self.registration_url = reverse("user:registration")
        self.login_url = reverse("user:login")
        self.logout_url = reverse("user:logout")

    def test_registration_get(self):
        response = self.client.get(self.registration_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user/user_registration.html")

    def test_logout_get(self):
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/main.html")

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user/user_login.html")

    def test_registration_post(self):
        response = self.client.post(
            self.registration_url,
            {
                "username": self.data,
                "firstname": self.data,
                "lastname": self.data,
                "psw": self.data,
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(User.objects.last().username, self.data)
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, True)

    def test_logout_post(self):
        response = self.client.post(
            self.registration_url,
            {
                "username": self.data,
                "firstname": self.data,
                "lastname": self.data,
                "psw": self.data,
            },
        )
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, True)
        response = self.client.post(self.logout_url)
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, False)

    def test_login_post(self):
        self.client.post(
            self.registration_url,
            {
                "username": self.data,
                "firstname": self.data,
                "lastname": self.data,
                "psw": self.data,
            },
        )
        self.client.post(self.logout_url)
        response = self.client.post(
            self.login_url, {"username": self.data, "psw": self.data}
        )
        self.assertEquals(response.status_code, 200)
        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, True)

    def random_register_data(self):
        return "".join(random.choice(string.printable) for i in range(8))
