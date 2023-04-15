from django.shortcuts import render, get_object_or_404, redirect
from .models import Airport, Passager, Flight
import pandas as pd
import datetime
import random
from faker import Faker
fake=Faker()

# Create your views here.
def index(request):
    context = {
        "airport": Airport.objects.all(),
        "passager":Passager.objects.all(),
        "flight":Flight.objects.all(),
        }
    return render(request, template_name="airline/main.html", context=context)

def passager(request, passager_id):
    passager ={"passager": get_object_or_404(Passager, pk=passager_id)}
    return render(request, template_name="airline/passager.html", context=passager)

def flight(request, fli_id):
    flight = {"flight": get_object_or_404(Flight, pk=fli_id)}
    return render(request, template_name="airline/flight.html", context=flight)

def airport(request, airport_id):
    airport= {"airport": get_object_or_404(Airport, pk=airport_id)}
    return render(request, template_name="airline/airport.html", context=airport)

def upload_airport(request):
    csv_file = pd.read_csv("airline/static/airline/Airports.csv", encoding="ISO-8859-1")
    airports = []
    if request.method == "POST":
        for index, row in csv_file.iterrows():
            if index < int(request.POST['vol']):
                airport = Airport(
                    airport_id=row[0],
                    name=row[1],
                    city=row[2],
                    country=row[3],
                    latitude=row[6],
                    longitude=row[7]
                )
                airports.append(airport)
            else:
                break
        Airport.objects.bulk_create(airports)
        return redirect('airline:index')
    return redirect('airline:index')

def upload_flight(request):
    flights = []
    if request.method == "POST":
        airports = Airport.objects.all()
        num_flights = int(request.POST['quan'])
        for i in range(num_flights):
            start = random.choice(airports)
            destination = random.choice(airports.exclude(airport_id=start.airport_id))
            date = datetime.date(random.randint(2022, 2030), random.randint(1, 12), random.randint(1, 28))
            flight = Flight(start=start, destination=destination, date=date, flight_number=i+1)
            flights.append(flight)
        Flight.objects.bulk_create(flights)
        return redirect('airline:index')
    return redirect('airline:index')