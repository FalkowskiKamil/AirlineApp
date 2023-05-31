from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.urls import reverse
from .models import Airport, Flight, Route, Passager
from . import data_manager, map_creator

# Create your views here.
def main(request):
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {"countries": countries, "routes": Route.objects.all()}
    return render(request, template_name="airline/main_user.html", context=context)


def staff(request):
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {
        "airport": Airport.objects.all(),
        "passager": Passager.objects.all(),
        "flight": Flight.objects.all().order_by("date"),
        "countries": countries,
    }
    return render(request, template_name="airline/main_staff.html", context=context)


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
    context = {"flight": flight, "map": map._repr_html_()}
    return render(request, template_name="airline/flight.html", context=context)


def flight_record(request, passager_id, flight_id):
    if request.method == "POST":
        passager = get_object_or_404(Passager, pk=passager_id)
        flight = get_object_or_404(Flight, pk=flight_id)
        if flight.passengers.filter(id=passager.id).exists():
            return HttpResponseBadRequest(
                "The passenger is already booked on this flight."
            )
        flight.passengers.add(passager)
        return redirect(reverse("airline:flight", args=[flight.id]))
    else:
        return HttpResponseBadRequest("Invalid request method.")


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


def add_data(request):
    context={}
    if request.method == "POST":
        match list(request.POST.keys())[1]:
            case "airport":
                data_manager.upload_airport(request.POST)
                context={"message": "Succesfuly loaded airport!"}
            case "flight":
                data_manager.upload_flight(request.POST)
                context={"message": "Succesfuly loaded flight!"}
            case "passager":
                data_manager.upload_passager(request.POST)
                context={"message": "Succesfuly loaded passager"}
    return render(request, template_name="airline/add_data.html", context=context)
