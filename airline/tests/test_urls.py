from django.test import SimpleTestCase
from django.urls import reverse, resolve
from airline.views import (
    main,
    country_map,
    airport,
    routes,
    flight,
    passager,
    full_map,
    full_data_user,
    full_data_staff,
    add_data,
)


class TestUrls(SimpleTestCase):
    def test_main_url_is_resolved(self):
        url = reverse("airline:main")
        self.assertEquals(resolve(url).func, main)

    def test_country_map_url_is_resolved(self):
        url = reverse("airline:country_map")
        self.assertEquals(resolve(url).func, country_map)

    def test_airport_url_is_resolved(self):
        url = reverse("airline:airport", kwargs={"airport_id": 1})
        self.assertEquals(resolve(url).func, airport)

    def test_routes_url_is_resolved(self):
        url = reverse("airline:routes", kwargs={"route_id": 1})
        self.assertEquals(resolve(url).func, routes)

    def test_flight_url_is_resolved(self):
        url = reverse("airline:flight", kwargs={"fli_id": 1})
        self.assertEquals(resolve(url).func, flight)

    def test_passager_url_is_resolved(self):
        url = reverse("airline:passager", kwargs={"passager_id": 1})
        self.assertEquals(resolve(url).func, passager)

    def test_full_map_url_is_resolved(self):
        url = reverse("airline:full_map")
        self.assertEquals(resolve(url).func, full_map)

    def test_full_data_user_url_is_resolved(self):
        url = reverse("airline:full_data_user")
        self.assertEquals(resolve(url).func, full_data_user)

    def test_full_data_staff_url_is_resolved(self):
        url = reverse("airline:full_data_staff")
        self.assertEquals(resolve(url).func, full_data_staff)

    def test_add_data_url_is_resolved(self):
        url = reverse("airline:add_data")
        self.assertEquals(resolve(url).func, add_data)
