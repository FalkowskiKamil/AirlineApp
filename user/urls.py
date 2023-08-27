from django.urls import path
from . import views


app_name = "user"
urlpatterns = [
    path("registration/", views.registration_request, name="registration_request"),
    path("login/", views.login_request, name="login_request"),
    path("logout/", views.logout_request, name="logout_request"),
]
