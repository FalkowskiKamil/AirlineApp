from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.urls import reverse
from .models import Airport, Flight, Route, Passager
from . import data_manager
import folium
from folium.vector_layers import PolyLine

# Create your views here.
def main(request):
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {"countries": countries, "routes": Route.objects.all()}
    return render(request, template_name="airline/main_user.html", context=context)


def staff(request):
    countries = set(Airport.objects.values_list("country", flat=True))
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
        "countries": set(Airport.objects.values_list("country", flat=True)),
    }
    return render(request, template_name="airline/passager.html", context=context)


def flight(request, fli_id):
    flight = get_object_or_404(Flight, pk=fli_id)
    start_airport = flight.start
    dest_airport = flight.destination
    map = folium.Map(
        location=[start_airport.latitude, start_airport.longitude],
        zoom_start=6,
        height=250,
    )
    folium.Marker(
        location=[start_airport.latitude, start_airport.longitude],
        popup=f"Start: {start_airport.name}",
        icon=folium.Icon(color="green"),
    ).add_to(map)
    folium.Marker(
        location=[dest_airport.latitude, dest_airport.longitude],
        popup=f"Destination: {dest_airport.name}",
        icon=folium.Icon(color="red"),
    ).add_to(map)
    line = PolyLine(
        locations=[
            [start_airport.latitude, start_airport.longitude],
            [dest_airport.latitude, dest_airport.longitude],
        ],
        color="blue",
        weight=2,
        opacity=10,
    )
    line.add_to(map)
    context = {"flight": flight, "map": map._repr_html_()}
    return render(request, template_name="airline/flight.html", context=context)


def airport(request, airport_id):
    airport = get_object_or_404(Airport, pk=airport_id)
    map = folium.Map(
        location=[airport.latitude, airport.longitude], zoom_start=10, height=250
    )
    folium.Marker(
        location=[airport.latitude, airport.longitude], popup=airport.name
    ).add_to(map)
    context = {
        "airport": airport,
        "map": map._repr_html_(),
        "countries": set(Airport.objects.values_list("country", flat=True)),
    }
    return render(request, template_name="airline/airport.html", context=context)


def routes(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    start_airport = route.start
    dest_airport = route.destination
    map = folium.Map(
        location=[start_airport.latitude, start_airport.longitude],
        zoom_start=6,
        height=250,
    )
    folium.Marker(
        location=[start_airport.latitude, start_airport.longitude],
        popup=f"Start: {start_airport.name}",
        icon=folium.Icon(color="green"),
    ).add_to(map)
    folium.Marker(
        location=[dest_airport.latitude, dest_airport.longitude],
        popup=f"Destination: {dest_airport.name}",
        icon=folium.Icon(color="red"),
    ).add_to(map)
    line = PolyLine(
        locations=[
            [start_airport.latitude, start_airport.longitude],
            [dest_airport.latitude, dest_airport.longitude],
        ],
        color="blue",
        weight=2,
        opacity=10,
    )
    line.add_to(map)
    context = {"route": route, "map": map._repr_html_()}
    return render(request, template_name="airline/route.html", context=context)


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

def add_data(request):
    context={}
    if request.method == "POST":
        if "airport" in request.POST:
            context={'message': 'Updated!'}
            data_manager.upload_airport(request.POST)
            context['message'] = "Succesfuly loaded airport"
        elif "flight" in request.POST:
            data_manager.upload_flight(request.POST)
            context['message'] = "Succesfuly loaded flight"
        elif "passager" in request.POST:
            data_manager.upload_passager(request.POST)
            context['message'] = "Succesfuly loaded passager"
    return render(request, template_name="airline/add_data.html", context=context)
