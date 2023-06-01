from .models import Flight, Passager, Airport, Route
from django.shortcuts import get_object_or_404, redirect
import pandas as pd
import datetime
import random
from faker import Faker

fake = Faker()

def upload_passager(request):
    passagers = []
    flights = Flight.objects.all()
    num_passager = int(request.get("passager"))
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

def upload_flight(request):
    airports = Airport.objects.all()
    num_flights = int(request.get('flight'))
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
            route, created = Route.objects.get_or_create(
            start=start_airport, destination=dest_airport
            )
            route.flights.set(flights)

def upload_airport(request):
    csv_file = pd.read_csv("airline/static/airline/Airports.csv", encoding="ISO-8859-1")
    airports = []
    existing_airport_ids = [airport.airport_id for airport in Airport.objects.all()]
    max_vol = int(request.get('airport'))
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

def sign_for_flight(passager_id, flight_id):
    passager = get_object_or_404(Passager, pk=passager_id)
    flight = get_object_or_404(Flight, pk=flight_id)
    flight.passengers.add(passager)