from django.test import TestCase, Client
# Create your tests here.
from django.urls import reverse
from .models import Airport, Flight, Route, Passager
from .views import main, staff, passager, flight, airport, routes
from django.utils import timezone

class AirportModelTests(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create(airport_id=1, name="Test Airport", city="Test City", country="Test Country", latitude=1.0, longitude=1.0)
        
    def test_airport_str(self):
        self.assertEqual(str(self.airport), "Test Airport")

class FlightModelTests(TestCase):
    def setUp(self):
        self.start_airport = Airport.objects.create(airport_id=1, name="Start Airport", city="Start City", country="Start Country", latitude=1.0, longitude=1.0)
        self.dest_airport = Airport.objects.create(airport_id=2, name="Dest Airport", city="Dest City", country="Dest Country", latitude=1.0, longitude=1.0)
        self.flight = Flight.objects.create(start=self.start_airport, destination=self.dest_airport, date=timezone.now())
        
    def test_flight_str(self):
        self.assertEqual(str(self.flight), f"{self.flight.id}")
        
    def test_flight_formatted_date(self):
        formatted_date = self.flight.formatted_date()
        self.assertEqual(formatted_date, self.flight.date.strftime("%d-%m-%Y"))

    def test_flight_clean_method(self):
        with self.assertRaises(ValueError):
            flight = Flight(start=self.start_airport, destination=self.start_airport, date=timezone.now())
            flight.clean()

class RouteModelTests(TestCase):
    def setUp(self):
        self.start_airport = Airport.objects.create(airport_id=1, name="Start Airport", city="Start City", country="Start Country", latitude=1.0, longitude=1.0)
        self.dest_airport = Airport.objects.create(airport_id=2, name="Dest Airport", city="Dest City", country="Dest Country", latitude=2.0, longitude=2.0)
        self.flight = Flight.objects.create(start=self.start_airport, destination=self.dest_airport, date=timezone.now())
        self.route = Route.objects.create(start=self.start_airport, destination=self.dest_airport)

    def test_route_str(self):
        self.assertEqual(str(self.route), f"{self.route.id}")

    def test_route_has_flight(self):
        self.route.flights.add(self.flight)
        self.assertIn(self.flight, self.route.flights.all())

class PassagerModelTests(TestCase):
    def setUp(self):
        self.passenger = Passager.objects.create(first_name="John", surname="Doe")
        self.start_airport = Airport.objects.create(airport_id=1, name="Start Airport", city="Start City", country="Start Country", latitude=1.0, longitude=1.0)
        self.dest_airport = Airport.objects.create(airport_id=2, name="Dest Airport", city="Dest City", country="Dest Country", latitude=1.0, longitude=1.0)
        self.flight = Flight.objects.create(start=self.start_airport, destination=self.dest_airport, date=timezone.now())
        
    def test_passenger_str(self):
        self.passenger = Passager.objects.create(first_name="John", surname="Doe")
        self.assertEqual(str(self.passenger), "('John', 'Doe')")
                         


    def test_passenger_has_flight(self):
        self.passenger.flights.add(self.flight)
        self.assertIn(self.flight, self.passenger.flights.all())

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        # Create some objects to use in the tests
        self.airport = Airport.objects.create(airport_id=1, name="Test Airport", city="Test City", country="Test Country", latitude=1.0, longitude=1.0)
        self.passenger = Passager.objects.create(first_name="John", surname="Doe")
        self.start_airport = Airport.objects.create(airport_id=2, name="Start Airport", city="Start City", country="Start Country", latitude=1.0, longitude=1.0)
        self.dest_airport = Airport.objects.create(airport_id=3, name="Dest Airport", city="Dest City", country="Dest Country", latitude=1.0, longitude=1.0)
        self.flight = Flight.objects.create(start=self.start_airport, destination=self.dest_airport, date=timezone.now())
        self.route = Route.objects.create(start=self.start_airport, destination=self.dest_airport)


    def test_main_view(self):
        url = reverse("airline:main")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/main_user.html")
        self.assertIn("countries", response.context)
        self.assertIn("routes", response.context)

    def test_staff_view(self):
        url = reverse("airline:staff")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/main_staff.html")
        self.assertIn("airport", response.context)
        self.assertIn("passager", response.context)
        self.assertIn("flight", response.context)
        self.assertIn("countries", response.context)

    def test_passager_view(self):
        url = reverse("airline:passager", args=[self.passenger.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/passager.html")
        self.assertIn("passager", response.context)
        self.assertIn("countries", response.context)

    def test_flight_view(self):
        url = reverse("airline:flight", args=[self.flight.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/flight.html")
        self.assertIn("flight", response.context)
        self.assertIn("map", response.context)

    def test_airport_view(self):
        url = reverse("airline:airport", args=[self.airport.airport_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/airport.html")
        self.assertIn("airport", response.context)
        self.assertIn("map", response.context)
        self.assertIn("countries", response.context)

    def test_routes_view(self):
        url = reverse("airline:routes", args=[self.route.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/route.html")
        self.assertIn("route", response.context)
        self.assertIn("map", response.context)