from django.test import TestCase
from django.contrib.admin import AdminSite
from django.utils import timezone
from ..admin import AirportAdmin, FlightAdmin, PassagerAdmin, RouteAdmin
from ..models import Airport, Flight, Passager, Route

class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
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
    def test_airport_admin(self):
        airport_admin = AirportAdmin(model=self.airport1, admin_site=self.site)
        self.assertEqual(airport_admin.list_display[0], "name")
        self.assertEqual(airport_admin.list_display[1], "city")
        self.assertEqual(airport_admin.list_display[2], "country")
        
    def test_flight_admin(self):
        flight = Flight.objects.create(start=self.airport1, destination=self.airport2, date=timezone.now())
        flight_admin = FlightAdmin(model=flight, admin_site=self.site)
        self.assertEqual(flight_admin.list_display[0], "id")
        self.assertEqual(flight_admin.list_display[1], "start")
        self.assertEqual(flight_admin.list_display[2], "destination")
        
    def test_passager_admin(self):
        passager = Passager.objects.create(first_name="John", surname="Doe")
        passager_admin = PassagerAdmin(model=passager, admin_site=self.site)
        self.assertEqual(passager_admin.list_display[0], "id")
        self.assertEqual(passager_admin.list_display[1], "first_name")
        self.assertEqual(passager_admin.list_display[2], "surname")
        
    def test_route_admin(self):
        route = Route.objects.create(start=self.airport1, destination=self.airport1)
        route_admin = RouteAdmin(model=route, admin_site=self.site)
        self.assertEqual(route_admin.list_display[0], "id")
        self.assertEqual(route_admin.list_display[1], "start")
        self.assertEqual(route_admin.list_display[2], "destination")
