from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView
from user.forms import AirlineRegistrationForm
from user import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path(
        "accounts/register/",
        RegistrationView.as_view(form_class=AirlineRegistrationForm),
        name="django_registration_register",
    ),    
    path('accounts/', include('django_registration.backends.activation.urls')),
]
