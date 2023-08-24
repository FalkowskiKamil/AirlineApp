from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from airline.models import Airport, Route, Flight, Passager


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.main_url = reverse("airline:main")
        self.country_map_url = reverse("airline:country_map")
        self.airport_start_model = Airport.objects.create(
            airport_id=1,
            name="start_name",
            city="start_city",
            country="start_country",
            latitude=0,
            longitude=0,
        )
        self.airport_destination_model = Airport.objects.create(
            airport_id=2,
            name="destination_name",
            city="destination_city",
            country="destination_country",
            latitude=45,
            longitude=45,
        )
        self.route_model = Route.objects.create(
            start=self.airport_start_model, destination=self.airport_destination_model
        )
        self.flight_model = Flight.objects.create(
            start=self.airport_start_model,
            destination=self.airport_destination_model,
            date=timezone.now(),
        )
        self.passager_model = Passager.objects.create(first_name="Tom", surname="Stone")
        self.airport_url = reverse("airline:airport", args=[1])
        self.routes_url = reverse("airline:routes", args=[1])
        self.flight_url = reverse("airline:flight", args=[1])
        self.passager_url = reverse("airline:passager", args=[1])
        self.full_map_url = reverse("airline:full_map")
        self.full_data_user_url = reverse("airline:full_data_user")
        self.full_data_staff_url = reverse("airline:full_data_staff")
        self.add_data_url = reverse("airline:add_data")

    def test_main_get(self):
        response = self.client.get(self.main_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/main.html")

    def test_country_map_get(self):
        response = self.client.get(self.country_map_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/full_map.html")

    def test_country_map_post_with_data(self):
        response = self.client.post(
            self.country_map_url,
            {
                "start_country": "start_country",
                "destination_country": "destination_country",
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/full_map.html")

    def test_airport_get(self):
        response = self.client.get(self.airport_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/airport.html")

    def test_routes_get(self):
        response = self.client.get(self.routes_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/route.html")

    def test_flight_get(self):
        response = self.client.get(self.flight_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/flight.html")

    def test_passager_map_get(self):
        response = self.client.get(self.passager_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/passager.html")

    def test_full_map_get(self):
        response = self.client.get(self.full_map_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/full_map.html")

    def test_full_data_user_get(self):
        response = self.client.get(self.full_data_user_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/full_data_user.html")

    def test_full_data_staff_get(self):
        response = self.client.get(self.full_data_staff_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/full_data_staff.html")

    def test_add_data_get(self):
        response = self.client.get(self.add_data_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "airline/add_data.html")

    def test_add_data_post_airport(self):
        response = self.client.post(
            self.add_data_url, {"add_airport_form": "True", "airport_country": "Poland"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Airport.objects.last().country, "Poland")

    def test_add_data_post_route(self):
        response = self.client.post(
            self.add_data_url,
            {"add_route_form": "True", "airport_start": "", "airport_destination": ""},
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Route.objects.last().id, 1)

    def test_add_data_post_flight(self):
        response = self.client.post(
            self.add_data_url, {"add_flight_form": "True", "route_id": ""}
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Flight.objects.last().id, 2)

    def test_add_data_post_passager(self):
        response = self.client.post(
            self.add_data_url,
            {"add_passager_form": "True", "passager_count": "1", "flight_id": ""},
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Flight.objects.last().id, 1)
