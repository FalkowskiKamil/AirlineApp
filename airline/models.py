from django.db import models
from django.conf import settings
from django.db.models.constraints import UniqueConstraint


# Create your models here.
class Airport(models.Model):
    """
    Model representing an airport.

    Attributes:
        airport_id (int): The ID of the airport (primary key).
        name (str): The name of the airport.
        city (str): The city where the airport is located.
        country (str): The country where the airport is located.
        latitude (float): The latitude coordinate of the airport.
        longitude (float): The longitude coordinate of the airport.
        departures (ManyToManyField): The flights departing from the airport.
        arrivals (ManyToManyField): The flights arriving at the airport.
    """

    airport_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    departures = models.ManyToManyField(
        "Flight", related_name="departure_airports", blank=True
    )
    arrivals = models.ManyToManyField(
        "Flight", related_name="arrival_airports", blank=True
    )

    def __str__(self):
        return f"{self.name}"


class Flight(models.Model):
    """
    Model representing a flight.

    Attributes:
        start (ForeignKey): The airport where the flight departs from.
        destination (ForeignKey): The airport where the flight arrives.
        date (DateTimeField): The date and time of the flight.
        passengers_flights (ManyToManyField): The passengers associated with the flight.
    """

    start = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departure_flights"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arrival_flights"
    )
    date = models.DateTimeField()
    passengers_flights = models.ManyToManyField(
        "Passager",
        through="FlightPassager",
        related_name="flights_passengers",
        blank=True,
    )

    def clean(self):
        if self.start == self.destination:
            raise ValueError("Start and destination cannot be the same.")

    def __str__(self):
        return f"{self.id}"

    def formatted_date(self):
        return self.date.strftime("%d-%m-%Y")

    def save(self, *args, **kwargs):
        super(Flight, self).save(*args, **kwargs)

        # Check if there is an existing route with the same start and destination
        existing_route = Route.objects.filter(
            start=self.start, destination=self.destination
        ).first()

        if existing_route:
            existing_route.flights.add(self)  # Add the flight to the existing route
        else:
            new_route = Route.objects.create(
                start=self.start, destination=self.destination
            )
            new_route.flights.add(self)


class Route(models.Model):
    """
    Model representing a flight route.

    Attributes:
        start (ForeignKey): The airport where the route starts.
        destination (ForeignKey): The airport where the route ends.
        flights (ManyToManyField): The flights associated with the route.
    """

    start = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departure_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arrival_routes"
    )
    flights = models.ManyToManyField(Flight, related_name="routes")

    def __str__(self):
        return f"{self.id}"


class Passager(models.Model):
    """
    Model representing a passenger.

    Attributes:
        user (ForeignKey): The user associated with the passenger.
        first_name (str): The first name of the passenger.
        surname (str): The surname of the passenger.
        flights (ManyToManyField): The flights associated with the passenger.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="passager_user",
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    flights = models.ManyToManyField(
        Flight, through="FlightPassager", related_name="passagers"
    )

    def __str__(self):
        return f"{self.first_name, self.surname}"


class FlightPassager(models.Model):
    """
    Model representing the relationship between flights and passengers.

    Attributes:
        flight (ForeignKey): The flight associated with the relationship.
        passager (ForeignKey): The passenger associated with the relationship.
        Meta (class): Class made to avoid non unique value
    """

    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="flight_passagers"
    )
    passager = models.ForeignKey(
        Passager, on_delete=models.CASCADE, related_name="flight_passagers"
    )

    class Meta:
        db_table = "airline_flight_passagers"
        constraints = [
            UniqueConstraint(
                fields=["flight", "passager"], name="unique_flight_passager"
            )
        ]
