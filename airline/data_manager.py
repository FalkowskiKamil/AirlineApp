from .models import Flight, Passager, Airport, FlightPassager
from django.shortcuts import get_object_or_404
import pandas as pd
from django.utils import timezone
import random
from manage import configure_logger
from faker import Faker
from mongo_connection import client

logger = configure_logger()
fake = Faker()


def upload_passager(request):
    """
    Create passagers to the database.

    Args:
        request (HttpRequest): The HTTP request object.

    """
    passagers = []
    flights = Flight.objects.all()
    num_passager = int(request.get("passager"))
    for i in range(num_passager):
        fullname = fake.name()
        name_parts = fullname.split(" ")
        # Rejection wrong value
        if len(name_parts) == 2:
            first_name, surname = name_parts
        else:
            first_name, surname = name_parts[1], name_parts[2]
        passager = Passager(first_name=first_name, surname=surname)
        passagers.append(passager)
    # Creating Passagers
    Passager.objects.bulk_create(passagers)
    # Connecting Passagers with flight
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
    """
    Create flight to the database.

    Args:
        request (HttpRequest): The HTTP request object.

    """
    airports = Airport.objects.all()
    num_flights = int(request.get("flight"))
    for i in range(num_flights):
        start = random.choice(airports)
        destination = random.choice(airports.exclude(airport_id=start.airport_id))
        date = fake.date_time_between(start_date=timezone.now(), end_date="+1y")
        flight = Flight.objects.create(start=start, destination=destination, date=date)
        flight.save()


def upload_airport(request):
    """
    Upload airport from database

    Args:
        request (HttpRequest): the HTTP request object.

    """
    db = client["AirlinesAppDB"]
    collection = db["Airport"]
    csv_file = pd.DataFrame(list(collection.find()))
    airports = []
    existing_airport_ids = [airport.airport_id for airport in Airport.objects.all()]
    max_vol = int(request.get("airport"))
    for i in range(max_vol):
        random_index = random.randint(0, len(csv_file) - 1)
        row = csv_file.iloc[random_index]
        # Checking duplication
        if row[0] not in existing_airport_ids:
            airport = Airport(
                airport_id=row[1],
                name=row[2],
                city=row[3],
                country=row[4],
                latitude=row[5],
                longitude=row[6],
            )
            airports.append(airport)
            existing_airport_ids.append(row[0])
    Airport.objects.bulk_create(airports)


def sign_for_flight(passager_id, flight_id):
    """
    Create connection flight-passager

    Args:
        passager_id (int): number of passager id
        flight_id (int): number of flight id

    """
    passager = get_object_or_404(Passager, pk=passager_id)
    flight = get_object_or_404(Flight, pk=flight_id)
    FlightPassager.objects.create(passager=passager, flight=flight)
    logger.debug(
        f"User: {passager.first_name} {passager.surname} register for flight {flight.id}"
    )
