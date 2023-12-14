from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from airline.api.views import AirportList, AirportDetail

urlpatterns = [
    path("airports/", AirportList.as_view(), name="api_airport_list"),
    path("airports/<int:pk>", AirportDetail.as_view(), name="api_airport_detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token)
]
