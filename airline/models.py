from django.conf import settings
from django.db import models
from django.db.models.constraints import UniqueConstraint


# Create your models here.
class Airport(models.Model):
    airport_id = models.IntegerField(primary_key=True)
    name= models.CharField(max_length=100)
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

    def __str__(self) -> str:
        return f"{self.name}"


class Flight(models.Model):
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

    def clean(self) -> None:
        if self.start == self.destination:
            raise ValueError("Start and destination cannot be the same.")

    def __str__(self) -> str:
        return f"Flight: {self.start} to {self.destination}, id: {self.id}" # type: ignore

    def formatted_date(self) -> str:
        return self.date.strftime("%d-%m-%Y")

    def save(self, *args, **kwargs) -> None:
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
    start = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departure_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arrival_routes"
    )
    flights = models.ManyToManyField(Flight, related_name="routes")

    def __str__(self) -> str:
        return f"Route: {self.start} {self.destination}" # type: ignore


class Passager(models.Model):
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

    def __str__(self) -> str:
        return f"{self.first_name, self.surname}"


class FlightPassager(models.Model):
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
