from django.shortcuts import render, get_object_or_404
from .models import Airport, Flight, Route, Passager
from . import data_manager, map_creator
from user.forms import MessageForm, MessageAnswerForm
from user.models import Message
from django.contrib.auth.models import User
from manage import configure_logger
import requests
import folium
import geoip2.database

logger = configure_logger()


# Create your views here.
def main(request):
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {
        "countries": countries,
    }
    return render(request, template_name="airline/main.html", context=context)


def country(request):
    context = {}
    if not request.POST["destination_country"]:
        route = Route.objects.filter(
            start__country=request.POST["start_country"].title()
        )
        context["countries"] = route
    else:
        route = Route.objects.filter(
            start__country=request.POST["start_country"].title(),
            destination__country=request.POST["destination_country"].title(),
        )
        context["countries"] = route
    return render(request, template_name="airline/country.html", context=context)


def full_data_user(request):
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {"countries": countries, "routes": Route.objects.all()}
    return render(request, template_name="airline/full_data_user.html", context=context)


def full_data_staff(request):
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {
        "airport": Airport.objects.all(),
        "passager": Passager.objects.all(),
        "flight": Flight.objects.all().order_by("date"),
        "countries": countries,
    }
    return render(
        request, template_name="airline/full_data_staff.html", context=context
    )


def passager(request, passager_id):
    passager = get_object_or_404(Passager, pk=passager_id)
    context = {
        "passager": passager,
        "countries": Airport.objects.values_list("country", flat=True).distinct(),
    }
    return render(request, template_name="airline/passager.html", context=context)


def flight(request, fli_id):
    flight = get_object_or_404(Flight, pk=fli_id)
    map = map_creator.create_map(flight.start, flight.destination)
    form = MessageForm(
        initial={
            "context": f"I would like to check out from my upcoming flight nr: {fli_id}"
        }
    )
    context = {"flight": flight, "map": map._repr_html_(), "form": form}
    if request.method == "POST":
        data_manager.sign_for_flight(request.user.passager_user.first().id, fli_id)
        context["message"] = "Signed up for flight!"
    return render(request, template_name="airline/flight.html", context=context)


def airport(request, airport_id):
    airport = get_object_or_404(Airport, pk=airport_id)
    map = map_creator.create_map(airport)
    context = {
        "airport": airport,
        "map": map._repr_html_(),
        "countries": Airport.objects.values_list("country", flat=True).distinct(),
    }
    return render(request, template_name="airline/airport.html", context=context)


def routes(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    map = map_creator.create_map(route.start, route.destination)
    context = {"route": route, "map": map._repr_html_()}
    return render(request, template_name="airline/route.html", context=context)


def full_map(request):
    route = Route.objects.all()
    map = map_creator.create_full_map(route)
    context = {"map": map._repr_html_()}
    return render(request, template_name="airline/full_map.html", context=context)


def add_data(request):
    context = {}
    if request.method == "POST":
        match list(request.POST.keys())[1]:
            case "airport":
                data_manager.upload_airport(request.POST)
                context = {"message": "Succesfuly loaded airport!"}
            case "flight":
                data_manager.upload_flight(request.POST)
                context = {"message": "Succesfuly loaded flight!"}
            case "passager":
                data_manager.upload_passager(request.POST)
                context = {"message": "Succesfuly loaded passager"}
    return render(request, template_name="airline/add_data.html", context=context)
