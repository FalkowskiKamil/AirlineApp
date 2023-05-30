from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.urls import reverse
from .models import Airport, Flight, Route, Passager
import folium
from folium.vector_layers import PolyLine
import pandas as pd
import datetime
import random
from faker import Faker

fake = Faker()


# Create your views here.
def main(request):
    countries = set(Airport.objects.values_list("country", flat=True))
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


def upload_airport(request):
    csv_file = pd.read_csv("airline/static/airline/Airports.csv", encoding="ISO-8859-1")
    airports = []
    existing_airport_ids = [airport.airport_id for airport in Airport.objects.all()]
    if request.method == "POST":
        max_vol = int(request.POST["vol"])
        for i in range(max_vol):
            random_index = random.randint(0, len(csv_file) - 1)
            row = csv_file.iloc[random_index]
            if row[0] not in existing_airport_ids:
                airport = Airport(
                    airport_id=row[0],
                    name=row[1],
                    city=row[2],
                    country=row[3],
                    latitude=row[6],
                    longitude=row[7],
                )
                airports.append(airport)
                existing_airport_ids.append(row[0])
        Airport.objects.bulk_create(airports)
        return redirect("airline:main")
    return redirect("airline:main")


def update_routes():
    # Get all unique start-destination pairs from flights
    routes = Flight.objects.values("start", "destination").distinct()
    for route in routes:
        # Try to get an existing route with this start-destination pair
        existing_route = Route.objects.filter(
            start=route["start"], destination=route["destination"]
        ).first()

        # If the route already exists, add the new flights to it
        if existing_route:
            flights = Flight.objects.filter(
                start=route["start"], destination=route["destination"]
            )
            existing_route.flights.add(*flights)

        # Otherwise, create a new route and assign all flights with this start-destination pair to it
        else:
            start_airport = get_object_or_404(Airport, pk=route["start"])
            dest_airport = get_object_or_404(Airport, pk=route["destination"])
            flights = Flight.objects.filter(
                start=start_airport, destination=dest_airport
            )
            new_route = Route(start=start_airport, destination=dest_airport)
            new_route.save()
            new_route.flights.set(flights)


def upload_flight(request):
    if request.method == "POST":
        airports = Airport.objects.all()
        num_flights = int(request.POST["quan"])
        for i in range(num_flights):
            start = random.choice(airports)
            destination = random.choice(airports.exclude(airport_id=start.airport_id))
            date = datetime.datetime(
                random.randint(2022, 2030),
                random.randint(1, 12),
                random.randint(1, 28),
                random.randint(0, 23),
                random.choice([0, 30]),
            )

            # Try to get an existing route with this start-destination pair
            existing_route = Route.objects.filter(
                start=start, destination=destination
            ).first()

            # If the route already exists, add the new flight to it
            if existing_route:
                flight = Flight.objects.create(
                    start=start, destination=destination, date=date
                )
                existing_route.flights.add(flight)
            # Otherwise, create a new route and assign the flight to it
            else:
                new_route = Route.objects.create(start=start, destination=destination)
                flight = Flight.objects.create(
                    start=start, destination=destination, date=date
                )
                new_route.flights.add(flight)

        return redirect("airline:main")
    return redirect("airline:main")


def upload_passager(request):
    passagers = []
    flights = Flight.objects.all()
    if request.method == "POST":
        num_passager = int(request.POST["quan"])
        for i in range(num_passager):
            fullname = fake.name()
            name_parts = fullname.split(" ")
            if len(name_parts) == 2:
                first_name, surname = name_parts
            else:
                continue
            passager = Passager(first_name=first_name, surname=surname)
            passagers.append(passager)
        Passager.objects.bulk_create(passagers)
        passager_flight_ids = [
            (passager.id, random.choice(flights).id) for passager in passagers
        ]
        Passager.flights.through.objects.bulk_create(
            [
                Passager.flights.through(passager_id=passager_id, flight_id=flight_id)
                for passager_id, flight_id in passager_flight_ids
            ]
        )

    return redirect("airline:main")


def add_data(request):
    return render(request, template_name="airline/add_data.html")
