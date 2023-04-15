from django.urls import path
from . import views


app_name = 'user'
urlpatterns =[
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
]