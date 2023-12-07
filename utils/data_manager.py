from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpRequest
from django.db.models import Q
from utils.mongo_connection import connect_to_mongodb
from utils.logger import configure_logger
from airline.models import Flight, Passager, Airport, FlightPassager, Route
from faker import Faker
import pandas as pd

logger = configure_logger()
fake = Faker()


def upload_airport(request: HttpRequest) -> str:
    countries = request.get("airport_country") # type: ignore
    _, df = connect_to_mongodb() # type: ignore
    if countries:
        airports_list: pd.DataFrame = df[(df.Country == countries)]
        try:
            existing_airport_name: list = [
                airport.name for airport in Airport.objects.filter(country=countries)
            ]
        except:
            existing_airport_name: list = []
    else:
        airports_list: pd.DataFrame = df
        existing_airport_name = [airport.name for airport in Airport.objects.all()]
    filtered_airports_list: list = airports_list[
        ~airports_list.Name.isin(existing_airport_name) # type: ignore
    ]
    if len(filtered_airports_list) > 0:
        airport_to_add = filtered_airports_list.sample() # type: ignore
        airport: object = Airport(
            airport_id=airport_to_add.iloc[0][1],
            name=airport_to_add.iloc[0][2],
            city=airport_to_add.iloc[0][3],
            country=airport_to_add.iloc[0][4],
            latitude=airport_to_add.iloc[0][5],
            longitude=airport_to_add.iloc[0][6],
        )
        airport.save()
        logger.debug(f"Added airport: {airport.name}")
        return f"Added {airport.name}"
    logger.debug(f"Country: {countries} have imported all of the avaible airport")
    return "No more Airport avaible in this area"


def upload_route(request: HttpRequest) -> str:
    start = request.get("airport_start") # type: ignore
    if start:
        start_airport: object = Airport.objects.get(airport_id=start)
    else:
        start_airport: object = Airport.objects.order_by("?").first()
    destination = request.get("airport_destination") # type: ignore
    if destination:
        destination_airport: object = Airport.objects.get(airport_id=destination)
    else:
        destination_airport: object = Airport.objects.filter(~Q(airport_id=start_airport.airport_id)).order_by("?").first() # type: ignore
    try:
        routes: object = Route.objects.get(start=start_airport, destination=destination_airport)
        logger.debug(f"Trying to make existing route {routes.id}") # type: ignore
        return "Route alredy exist"
    except:
        if start_airport != destination_airport:
            route: object = Route.objects.create(
                start=start_airport, destination=destination_airport
            )
            logger.debug(
                f"Make new route ({route.id}) from {route.start} to {route.destination}" # type: ignore
            )
            return f"Added new route ({route.id}) from {route.start} to {route.destination}" # type: ignore
        else:
            logger.debug(
                f"Trying to make route with this same start and destination ({start_airport})"
            )
            return "Start and destination cannot be this same!"


def upload_flight(request: HttpRequest) -> str:
    route_id: int = request.get("route_id") # type: ignore
    if route_id:
        route: object = Route.objects.get(id=route_id)
    else:
        route: object = Route.objects.order_by("?").first()
    flight_date: str = request.get("datetime") # type: ignore
    if flight_date:
        date: str = flight_date
    else:
        date: str = fake.date_time_between(start_date=timezone.now(), end_date="+1y")
    start: object = route.start # type: ignore
    destination: object = route.destination # type: ignore
    flight: object = Flight.objects.create(start=start, destination=destination, date=date)
    flight.save()
    logger.debug(f"Make new flight ({flight.id}) on route {route_id} with date {date}") # type: ignore
    return f"Succesfuly added new flight"


def upload_passager(request: HttpRequest) -> str:
    num_passager: int = int(request.get("passager_count")) # type: ignore
    flight_id: int = request.get("flight_id") # type: ignore
    if flight_id:
        flight: object = Flight.objects.get(id=flight_id)
    else:
        flight: object = Flight.objects.order_by("?").first()
    for i in range(num_passager):
        fullname: str = fake.name()
        name_parts: str = fullname.split(" ") # type: ignore
        # Rejection wrong value
        if len(name_parts) == 2:
            first_name, surname = name_parts
        else:
            first_name, surname = name_parts[1], name_parts[2]
        passager: object = Passager.objects.create(first_name=first_name, surname=surname)
        passager.flights.add(flight)
        passager.save()
    logger.debug(f"Make {num_passager} passagers")
    return f"Succesfuly added {num_passager} passagers!"


def sign_for_flight(passager_id: int, flight_id: int) -> None:
    passager: object = get_object_or_404(Passager, pk=passager_id)
    flight: object = get_object_or_404(Flight, pk=flight_id)
    FlightPassager.objects.create(passager=passager, flight=flight)
    logger.debug(
        f"User: {passager.first_name} {passager.surname} register for flight {flight.id}" # type: ignore
    )
