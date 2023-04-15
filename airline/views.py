from django.shortcuts import render, get_object_or_404
from .models import Airport, Passager, Flight
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

def test(request):
    from . import medical_data_visualizer
    x=fake.name()
    z=medical_data_visualizer.draw_cat_plot
    y=medical_data_visualizer.draw_heat_map

    context = {
        "imie":x,
    }
    return render(request, template_name="airline/test.html", context=context)

def flight(request, fli_id):
    flight = {"flight": get_object_or_404(Flight, pk=fli_id)}
    return render(request, template_name="airline/flight.html", context=flight)

def airport(request, airport_id):
    airport= {"airport": get_object_or_404(Airport, pk=airport_id)}
    return render(request, template_name="airline/airport.html", context=airport)