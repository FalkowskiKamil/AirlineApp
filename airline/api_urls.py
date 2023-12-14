from django.urls import path

from airline.api_views import airport_list, airport_detail

urlpatterns = [
    path("airports/", airport_list, name="api_airport_list"),
    path("airports/<int:pk>/", airport_detail, name="api_airport_detail"),
]