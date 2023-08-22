from django.urls import path
from . import views

app_name = "airline"
urlpatterns = [
    path("", views.main, name="main"),
    path("full_data_staff/", views.full_data_staff, name="full_data_staff"),
    path("passager/<int:passager_id>", views.passager, name="passager"),
    path("flight/<int:fli_id>", views.flight, name="flight"),
    path("airport/<int:airport_id>", views.airport, name="airport"),
    path("add_data/", views.add_data, name="add_data"),
    path("routes/<int:route_id>", views.routes, name="routes"),
    path("full_data_user", views.full_data_user, name="full_data_user"),
    path("full_map", views.full_map, name="full_map"),
    path("country/map", views.country_map, name="country_map")
]
