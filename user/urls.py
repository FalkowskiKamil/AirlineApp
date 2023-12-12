from django.urls import path, include
from . import views


app_name = "user"
urlpatterns = [
    path("registration/", views.registration_request, name="registration_request"),
    path("login/", views.login_request, name="login_request"),
    path("logout/", views.logout_request, name="logout_request"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),
]
