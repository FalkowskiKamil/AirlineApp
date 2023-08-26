from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .mongo_connection import connect_to_mongodb
from .logger import configure_logger
from airline.models import Flight, Passager, Airport, FlightPassager, Route
from faker import Faker

logger = configure_logger()
fake = Faker()


def upload_airport(request):
    countries = request.get("airport_country")
    _, df = connect_to_mongodb()
    if countries:
        airports_list = df[(df.Country == countries)]
        try:
            existing_airport_name = [
                airport.name for airport in Airport.objects.filter(country=countries)
            ]
        except:
            existing_airport_name = []
    else:
        airports_list = df
        existing_airport_name = [airport.name for airport in Airport.objects.all()]
    filtered_airports_list = airports_list[
        ~airports_list.Name.isin(existing_airport_name)
    ]
    if len(filtered_airports_list) > 0:
        airport_to_add = filtered_airports_list.sample()
        airport = Airport(
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
    else:
        logger.debug(f"Country: {countries} have imported all of the avaible airport")
        return "No more Airport avaible in this area"


def upload_route(request):
    start = request.get("airport_start")
    if start:
        start_airport = Airport.objects.get(airport_id=start)
    else:
        start_airport = Airport.objects.order_by("?").first()
    destination = request.get("airport_destination")
    if destination:
        destination_airport = Airport.objects.get(airport_id=destination)
    else:
        destination_airport = Airport.objects.filter(~Q(airport_id=start_airport.airport_id)).order_by("?").first()
    try:
        routes = Route.objects.get(start=start_airport, destination=destination_airport)
        logger.debug(f"Trying to make existing route {routes.id}")

        return "Route alredy exist"
    except:
        if start_airport != destination_airport:
            route = Route.objects.create(
                start=start_airport, destination=destination_airport
            )
            logger.debug(
                f"Make new route ({route.id}) from {route.start} to {route.destination}"
            )
            return f"Added new route ({route.id}) from {route.start} to {route.destination}"
        else:
            logger.debug(
                f"Trying to make route with this same start and destination ({start_airport})"
            )
            return "Start and destination cannot be this same!"


def upload_flight(request):
    route_id = request.get("route_id")
    if route_id:
        route = Route.objects.get(id=route_id)
    else:
        route = Route.objects.order_by("?").first()
        print("Random")
    flight_date = request.get("datetime")
    if flight_date:
        date = flight_date
    else:
        date = fake.date_time_between(start_date=timezone.now(), end_date="+1y")
    start = route.start
    destination = route.destination
    flight = Flight.objects.create(start=start, destination=destination, date=date)
    flight.save()
    logger.debug(f"Make new flight ({flight.id}) on route {route_id} with date {date}")
    return f"Succesfuly added new flight"


def upload_passager(request):
    num_passager = int(request.get("passager_count"))
    flight_id = request.get("flight_id")
    if flight_id:
        flight = Flight.objects.get(id=flight_id)
    else:
        flight = Flight.objects.order_by("?").first()
    for i in range(num_passager):
        fullname = fake.name()
        name_parts = fullname.split(" ")
        # Rejection wrong value
        if len(name_parts) == 2:
            first_name, surname = name_parts
        else:
            first_name, surname = name_parts[1], name_parts[2]
        passager = Passager.objects.create(first_name=first_name, surname=surname)
        passager.flights.add(flight)
        passager.save()
    logger.debug(f"Make {num_passager} passagers")
    return f"Succesfuly added {num_passager} passagers!"


def sign_for_flight(passager_id, flight_id):
    passager = get_object_or_404(Passager, pk=passager_id)
    flight = get_object_or_404(Flight, pk=flight_id)
    FlightPassager.objects.create(passager=passager, flight=flight)
    logger.debug(
        f"User: {passager.first_name} {passager.surname} register for flight {flight.id}"
    )
    return f"Succesfuly signed for flight {flight.id}"
