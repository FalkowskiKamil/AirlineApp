from django.db import models
import pandas as pd
import csv

# Create your models here.
class Airport(models.Model):
    airport_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name}"

class Flight(models.Model):
    flight_number = models.IntegerField()
    start = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    date = models.DateTimeField()

    def clean(self):
        if self.start == self.destination:
            raise ValueError("Start and destination cannot be the same.")
        
    def __str__(self):
        return f"Flight {self.flight_number}"

class Passager(models.Model):
    first_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    flights = models.ManyToManyField(Flight, related_name='passengers')

    def __str__(self):
        return f"{self.first_name} {self.surname}"
