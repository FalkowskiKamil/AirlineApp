from django.test import TestCase
from ..map_creator import (
    create_map,
    create_full_map,
    get_random_color,
    meridian_calculator,
)
from airline.models import Airport, Route


class MapTest(TestCase):
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
        route1 = Route.objects.create(start=self.airport1, destination=self.airport2)
        route2 = Route.objects.create(start=self.airport2, destination=self.airport1)
        self.route_list = [route1, route2]

    def test_create_map_no_data(self):
        with self.assertRaises(TypeError):
            create_map()

    def test_create_map_one_airport(self):
        map = create_map(self.airport1)
        self.assertEquals(
            map.location, [self.airport1.latitude, self.airport1.longitude]
        )
        self.assertEquals(map.options["zoom"], 10)
        self.assertEquals(map.height, (250.0, "px"))

    def test_create_map_two_airport(self):
        map = create_map(self.airport1, self.airport2)
        # Calculating center
        center_latitude = (self.airport1.latitude + self.airport2.latitude) / 2
        center_longitude = (self.airport1.longitude + self.airport2.longitude) / 2
        self.assertEquals(map.location, [center_latitude, center_longitude])
        self.assertEquals(map.options["zoom"], 4)
        self.assertEquals(map.height, (250.0, "px"))
        self.assertEquals(
            map.get_bounds()[0], [self.airport1.latitude, self.airport1.longitude]
        )
        self.assertEquals(
            map.get_bounds()[1], [self.airport2.latitude, self.airport2.longitude]
        )
        # Testing Polyline
        self.assertTrue(list(map._children)[3].startswith("poly_line"))

    def test_create_full_map_no_data(self):
        with self.assertRaises(TypeError):
            create_full_map()

    def test_create_full_map_with_data(self):
        map = create_full_map(self.route_list)
        self.assertEquals(map.location, [0, 0])
        self.assertEquals(map.options["zoom"], 2)
        self.assertEquals(
            map.get_bounds()[0], [self.airport1.latitude, self.airport1.longitude]
        )
        self.assertEquals(
            map.get_bounds()[1],
            [self.airport2.latitude + 0.01, self.airport2.longitude],
        )
        self.assertTrue(list(map._children)[3].startswith("poly_line"))

    def test_meridian_calculator(self):
        test_cases = [
            (170, 175),  # Closest when adding 360
            (175, 170),  # Closest when subtracting 360
            (180, 185),  # Closest without wrapping
        ]

        for airport_start, airport_destination in test_cases:
            result = meridian_calculator(airport_start, airport_destination)
            self.assertTrue(abs(result - airport_destination) <= 180)

    def test_get_random_color(self):
        random_color = get_random_color()
        self.assertTrue(random_color.startswith("#"))
        self.assertEqual(len(random_color), 7)

        color_int = int(random_color[1:], 16)
        self.assertGreaterEqual(color_int, 0)
        self.assertLessEqual(color_int, 0xFFFFFF)