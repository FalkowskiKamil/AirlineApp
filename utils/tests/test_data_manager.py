from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from ..data_manager import (
    upload_airport,
    upload_flight,
    upload_route,
    upload_passager,
    sign_for_flight,
)
from airline.models import Airport, Route, Flight, Passager


class TestDataManager(TestCase):
    def setUp(self):
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
        self.route = Route.objects.create(
            start=self.airport1, destination=self.airport2
        )
        self.passager = Passager.objects.create(
            first_name="Test_Name", surname="Surname"
        )

    def test_upload_airport_random_country(self):
        request = {"airport_country": ""}
        airport_count_before = len(Airport.objects.all())
        response = upload_airport(request)
        airport_count_after = len(Airport.objects.all())
        self.assertEquals(airport_count_before + 1, airport_count_after)
        self.assertTrue(response.startswith("Added"))

    def test_upload_airport_specific_country(self):
        request = {"airport_country": "Germany"}
        response = upload_airport(request)
        airport = Airport.objects.last()
        self.assertEquals(airport.country, "Germany")
        self.assertTrue(response.startswith("Added"))

    def test_upload_route_this_same_start_destination(self):
        route_count_before = len(Route.objects.all())
        request = {"airport_start": "1", "airport_destination": "1"}
        response = upload_route(request)
        route_count_after = len(Route.objects.all())
        self.assertEquals(response, "Start and destination cannot be this same!")
        self.assertEquals(route_count_before, route_count_after)

    def test_upload_route_random(self):
        Flight.objects.all().delete()
        Route.objects.all().delete()
        route_count_before = len(Route.objects.all())
        request = {"airport_start": "", "airport_destination": ""}
        response = upload_route(request)
        route_count_after = len(Route.objects.all())
        self.assertEquals(route_count_before + 1, route_count_after)
        self.assertIn(Route.objects.first().start.name, ["Airport 1", "Airport 2"])
        self.assertIn(
            Route.objects.first().destination.name, ["Airport 1", "Airport 2"]
        )
        self.assertTrue(response.startswith("Added"))

    def test_upload_route_with_data(self):
        Flight.objects.all().delete()
        Route.objects.all().delete()
        route_count_before = len(Route.objects.all())
        request = {"airport_start": "1", "airport_destination": "2"}
        response = upload_route(request)
        route_count_after = len(Route.objects.all())
        self.assertEquals(route_count_before + 1, route_count_after)
        self.assertEquals(Route.objects.first().start.name, "Airport 1")
        self.assertEquals(Route.objects.first().destination.name, "Airport 2")
        self.assertTrue(response.startswith("Added"))

    def test_upload_route_duplicate_route(self):
        Flight.objects.all().delete()
        Route.objects.all().delete()
        request = {"airport_start": "1", "airport_destination": "2"}
        response_setting = upload_route(request)
        response_repeat = upload_route(request)
        self.assertEquals(response_repeat, "Route alredy exist")

    def test_upload_flight_random(self):
        flight_count_before = len(Flight.objects.all())
        request = {"route_id": "", "datetime": ""}
        response = upload_flight(request)
        flight_count_after = len(Flight.objects.all())
        self.assertEquals(flight_count_before + 1, flight_count_after)
        self.assertIn(Flight.objects.first().start.name, ["Airport 1", "Airport 2"])
        self.assertIn(
            Flight.objects.first().destination.name, ["Airport 1", "Airport 2"]
        )
        self.assertEquals(response, "Succesfuly added new flight")

    def test_upload_flight_specific_data(self):
        flight_count_before = len(Flight.objects.all())
        time = timezone.now()
        request = {"route_id": "1", "datetime": time}
        response = upload_flight(request)
        flight_count_after = len(Flight.objects.all())
        flight = Flight.objects.first()
        self.assertEquals(flight_count_before + 1, flight_count_after)
        self.assertIn(flight.start.name, ["Airport 1", "Airport 2"])
        self.assertIn(flight.destination.name, ["Airport 1", "Airport 2"])
        self.assertEquals(flight.routes.first().id, 1)
        self.assertEquals(response, "Succesfuly added new flight")
        time_diffrence = abs(flight.date - time)
        tolerance = timedelta(seconds=1)
        self.assertTrue(time_diffrence <= tolerance)


    def test_upload_passager_random(self):
        request = {"passager_count": "1", "flight_id": ""}
        passager_count_before = len(Passager.objects.all())
        response = upload_passager(request)
        passager_count_after = len(Passager.objects.all())
        passager = Passager.objects.last()
        self.assertEquals(passager_count_before + 1, passager_count_after)
        self.assertEquals(
            Flight.objects.last().passengers_flights.last().first_name,
            passager.first_name,
        )
        self.assertEquals(response, f"Succesfuly added 1 passagers!")

    def test_upload_passager_specific(self):
        request = {"passager_count": "5", "flight_id": "1"}
        passager_count_before = len(Passager.objects.all())
        response = upload_passager(request)
        passager_count_after = len(Passager.objects.all())
        passager = Passager.objects.last()
        self.assertEquals(passager_count_before + 5, passager_count_after)
        self.assertEquals(
            Flight.objects.last().passengers_flights.last().first_name,
            passager.first_name,
        )
        self.assertEquals(response, f"Succesfuly added 5 passagers!")

    def test_sign_for_flight(self):
        registered_flight_count_before = len(self.passager.flights.all())
        registered_passager_count_before = len(self.flight.passengers_flights.all())
        response = sign_for_flight(self.passager.id, self.flight.id)
        registered_flight_count_after = len(self.passager.flights.all())
        registered_passager_count_after = len(self.flight.passengers_flights.all())
        self.assertEquals(
            registered_flight_count_before + 1, registered_flight_count_after
        )
        self.assertEquals(
            registered_passager_count_before + 1, registered_passager_count_after
        )
        self.assertEquals(response, f"Succesfuly signed for flight {self.flight.id}")
        self.assertEquals(self.flight.passengers_flights.last(), self.passager)
