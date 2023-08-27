from django.test import TestCase
from django.utils import timezone
from ..models import Airport, Flight, Route, Passager, FlightPassager
from django.contrib.auth.models import User


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.airport1 = Airport.objects.create(
            airport_id=1,
            name="Airport 1",
            city="City 1",
            country="Country 1",
            latitude=12.34,
            longitude=56.78,
        )
        self.airport2 = Airport.objects.create(
            airport_id=2,
            name="Airport 2",
            city="City 2",
            country="Country 2",
            latitude=23.45,
            longitude=67.89,
        )
        self.flight = Flight.objects.create(
            start=self.airport1, destination=self.airport2, date=timezone.now()
        )
        self.passenger = Passager.objects.create(
            user=self.user, first_name="John", surname="Smith"
        )
        self.flight_passager = FlightPassager.objects.create(
            flight=self.flight, passager=self.passenger
        )

    def test_flight_str(self):
        self.assertEqual(str(self.flight), str(self.flight.pk))

    def test_passager_str(self):
        expected_str = f"('{self.passenger.first_name}', '{self.passenger.surname}')"
        self.assertEqual(str(self.passenger), expected_str)

    def test_route_created(self):
        route = Route.objects.get(start=self.airport1, destination=self.airport2)
        self.assertIsNotNone(route)

    def test_passager_flights(self):
        self.assertEqual(self.passenger.flights.count(), 1)
        self.assertEqual(self.passenger.flights.first(), self.flight)

    def test_flight_passager_created(self):
        self.assertEqual(self.flight.flight_passagers.count(), 1)
        self.assertEqual(self.flight.flight_passagers.first(), self.flight_passager)

    def test_clean_method(self):
        with self.assertRaises(ValueError):
            flight = Flight(
                start=self.airport1, destination=self.airport1, date=timezone.now()
            )
            flight.full_clean()

    def test_formatted_date(self):
        formatted_date = self.flight.formatted_date()
        self.assertEqual(formatted_date, self.flight.date.strftime("%d-%m-%Y"))

    def test_existing_route(self):
        flight2 = Flight.objects.create(
            start=self.airport1, destination=self.airport2, date=timezone.now()
        )
        route = Route.objects.get(start=self.airport1, destination=self.airport2)
        self.assertEqual(route.flights.count(), 2)
        self.assertIn(self.flight, route.flights.all())
        self.assertIn(flight2, route.flights.all())

    def test_unique_flight_passager_constraint(self):
        with self.assertRaises(Exception):
            FlightPassager.objects.create(flight=self.flight, passager=self.passenger)
