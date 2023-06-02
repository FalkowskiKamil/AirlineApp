from .models import Flight, Passager, Airport
from django.shortcuts import get_object_or_404
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
    num_flights = int(request.get("flight"))
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

        flight = Flight.objects.create(start=start, destination=destination, date=date)
        flight.save()


def upload_airport(request):
    csv_file = pd.read_csv("airline/static/airline/Airports.csv", encoding="ISO-8859-1")
    airports = []
    existing_airport_ids = [airport.airport_id for airport in Airport.objects.all()]
    max_vol = int(request.get("airport"))
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
