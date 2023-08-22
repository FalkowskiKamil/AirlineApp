from django.test import TestCase, Client, RequestFactory
from faker import Faker

# Create your tests here.
from .models import Airport, Flight, Passager
from django.utils import timezone
import unittest
import folium
from ..utils.map_creator import create_map
from .urls import *
from .data_manager import *
from .views import *


class ModelTestCase(TestCase):
    def setUp(self):
        self.date = timezone.now()
        self.airport_start = Airport.objects.create(
            airport_id=1,
            name="Start Airport",
            city="Start City",
            country="Start Country",
            latitude=1.0,
            longitude=1.0,
        )
        self.airport_destination = Airport.objects.create(
            airport_id=2,
            name="Dest Airport",
            city="Dest City",
            country="Dest Country",
            latitude=1.0,
            longitude=1.0,
        )

    def test_airport(self):
        airport = Airport(
            airport_id=1,
            name="Name",
            city="City",
            country="Country",
            latitude=1.0,
            longitude=1.0,
        )
        self.assertEqual(airport.name, "Name")
        self.assertEqual(airport.city, "City")
        self.assertEqual(airport.country, "Country")
        self.assertEqual(airport.latitude, 1.0)
        self.assertEqual(airport.longitude, 1.0)

    def test_flight(self):
        flight = Flight.objects.create(
            start=self.airport_start,
            destination=self.airport_destination,
            date=self.date,
        )

        self.assertEqual(flight.start.name, "Start Airport")
        self.assertEqual(flight.destination.name, "Dest Airport")
        self.assertEqual(flight.date, self.date)
        self.assertFalse(flight.passengers_flights.exists())

    def test_route(self):
        flight = Flight.objects.create(
            start=self.airport_start,
            destination=self.airport_destination,
            date=self.date,
        )
        route = flight.routes.first()
        self.assertEqual(route.start.name, "Start Airport")
        self.assertEqual(route.destination.name, "Dest Airport")
        self.assertEqual(route.flights.first().id, int("1"))

    def test_passager(self):
        passenger = Passager.objects.create(first_name="John", surname="Doe")
        self.assertEqual(passenger.first_name, "John")
        self.assertEqual(passenger.surname, "Doe")


class MapTestCase(TestCase):
    def test_create_map(self):
        airport_start = Airport(
            name="Start Airport",
            latitude=1.0,
            longitude=1.0,
        )
        airport_dest = Airport(
            name="Destination Airport",
            latitude=2.0,
            longitude=2.0,
        )
        map = create_map(airport_start, airport_dest)
        self.assertIsInstance(map, folium.Map)
        self.assertEqual(map.location, [1.0, 1.0])
        self.assertEqual(map.options.get("zoom"), 10)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.airport_start = Airport.objects.create(
            airport_id=1,
            name="Start Airport",
            city="Start City",
            country="Start Country",
            latitude=1.0,
            longitude=1.0,
        )
        self.airport_destination = Airport.objects.create(
            airport_id=2,
            name="Dest Airport",
            city="Dest City",
            country="Dest Country",
            latitude=1.0,
            longitude=1.0,
        )
        self.flight = Flight.objects.create(
            start=self.airport_start,
            destination=self.airport_destination,
            date=timezone.now(),
        )
        self.route = self.flight.routes.first()
        self.passager = Passager.objects.create(first_name="John", surname="Doe")
        self.factory = RequestFactory()

    def test_main_view(self):
        request = self.factory.get("main")
        response = main(request)
        self.assertEqual(response.status_code, 200)

    def test_country_view(self):
        data = {"start_country": "Country 1", "destination_country": "Country 2"}
        request = self.factory.post("country", data)
        response = country(request)
        self.assertEqual(response.status_code, 200)

    def test_all_view(self):
        request = self.factory.get("all")
        response = all(request)
        self.assertEqual(response.status_code, 200)

    def test_staff_view(self):
        request = self.factory.get("staff")
        response = staff(request)
        self.assertEqual(response.status_code, 200)

    def test_passager_view(self):
        request = self.factory.get("passager")
        response = passager(request, self.passager.id)
        self.assertEqual(response.status_code, 200)

    def test_flight_view(self):
        request = self.factory.get("flight")
        response = flight(request, self.flight.id)
        self.assertEqual(response.status_code, 200)

    def test_airport_view(self):
        request = self.factory.get("airport")
        response = airport(request, self.airport_start.airport_id)
        self.assertEqual(response.status_code, 200)

    def test_routes_view(self):
        request = self.factory.get("routes")
        response = routes(request, self.route.id)
        self.assertEqual(response.status_code, 200)

    def test_add_data_view(self):
        request = self.factory.get("add_data")
        response = add_data(request)
        self.assertEqual(response.status_code, 200)


class DataManagerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.fake = Faker()
        self.airport_start = Airport.objects.create(
            airport_id=1,
            name="Start Airport",
            city="Start City",
            country="Start Country",
            latitude=1.0,
            longitude=1.0,
        )
        self.airport_destination = Airport.objects.create(
            airport_id=2,
            name="Dest Airport",
            city="Dest City",
            country="Dest Country",
            latitude=1.0,
            longitude=1.0,
        )
        self.flight = Flight.objects.create(
            start=self.airport_start,
            destination=self.airport_destination,
            date=timezone.now(),
        )

    def test_upload_passager(self):
        passager_count = Passager.objects.count()
        request = {"passager": 5}
        upload_passager(request)
        self.assertEqual(Passager.objects.count(), 5 + passager_count)

    def test_upload_flight(self):
        flight_count = Flight.objects.count()
        request = {"flight": 5}
        upload_flight(request)
        self.assertEqual(Flight.objects.count(), 5 + flight_count)

    def test_upload_airport(self):
        airport_count = Airport.objects.count()
        request = {"airport": 20}
        upload_airport(request)
        self.assertEqual(Airport.objects.count(), 20 + airport_count)

    def test_sign_for_flight(self):
        passager = Passager.objects.create(first_name="John", surname="Doe")
        flight = Flight.objects.create(
            start=self.airport_start,
            destination=self.airport_destination,
            date=timezone.now(),
        )
        passager_id = passager.id
        flight_id = flight.id
        sign_for_flight(passager_id, flight_id)
        flight_passager = FlightPassager.objects.filter(
            passager=passager, flight=flight
        ).first()
        self.assertIsNotNone(flight_passager)
        self.assertEqual(flight_passager.passager, passager)
        self.assertEqual(flight_passager.flight, flight)
