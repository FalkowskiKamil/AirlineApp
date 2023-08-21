from django.shortcuts import render, get_object_or_404
from .models import Airport, Flight, Route, Passager
from . import data_manager, map_creator
from manage import configure_logger
from utils.mongo_connection import connect_to_mongodb

logger = configure_logger()


# Create your views here.
def main(request):
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {
        "countries": countries,
    }
    return render(request, template_name="airline/main.html", context=context)


def country(request):
    context = {}
    if not request.POST["destination_country"]:
        route = Route.objects.filter(
            start__country=request.POST["start_country"].title()
        )
        context["countries"] = route
    else:
        route = Route.objects.filter(
            start__country=request.POST["start_country"].title(),
            destination__country=request.POST["destination_country"].title(),
        )
        context["countries"] = route
    return render(request, template_name="airline/country.html", context=context)


def full_data_user(request):
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {"countries": countries, "routes": Route.objects.all()}
    return render(request, template_name="airline/full_data_user.html", context=context)


def full_data_staff(request):
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {
        "airport": Airport.objects.all(),
        "passager": Passager.objects.all(),
        "flight": Flight.objects.all().order_by("date"),
        "countries": countries,
    }
    return render(
        request, template_name="airline/full_data_staff.html", context=context
    )


def passager(request, passager_id):
    passager = get_object_or_404(Passager, pk=passager_id)
    context = {
        "passager": passager,
        "countries": Airport.objects.values_list("country", flat=True).distinct(),
    }
    return render(request, template_name="airline/passager.html", context=context)


def flight(request, fli_id):
    flight = get_object_or_404(Flight, pk=fli_id)
    map = map_creator.create_map(flight.start, flight.destination)
    context = {"flight": flight, "map": map._repr_html_()}
    if request.method == "POST":
        data_manager.sign_for_flight(request.user.passager_user.first().id, fli_id)
        context["message"] = "Signed up for flight!"
    return render(request, template_name="airline/flight.html", context=context)


def airport(request, airport_id):
    airport = get_object_or_404(Airport, pk=airport_id)
    map = map_creator.create_map(airport)
    context = {
        "airport": airport,
        "map": map._repr_html_(),
        "countries": Airport.objects.values_list("country", flat=True).distinct(),
    }
    return render(request, template_name="airline/airport.html", context=context)


def routes(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    map = map_creator.create_map(route.start, route.destination)
    context = {"route": route, "map": map._repr_html_()}
    return render(request, template_name="airline/route.html", context=context)


def full_map(request):
    route = Route.objects.all()
    map = map_creator.create_full_map(route)
    context = {"map": map._repr_html_()}
    return render(request, template_name="airline/full_map.html", context=context)


def add_data(request):
    status_of_connection = connect_to_mongodb()
    context = {"message":status_of_connection[0]}
    flights_already_made = Flight.objects.all()
    routes_alredy_made = Route.objects.all()
    context['flights']=flights_already_made
    context['routes']=routes_alredy_made
    db = status_of_connection[1]
    db = sorted(db['Country'].unique())
    context['countries'] = db
    if request.method == "POST":
        if "add_airport_form" in request.POST:
            message = data_manager.upload_airport(request.POST)
            context["message"]= message
        elif "add_flight_form" in request.POST:
            data_manager.upload_flight(request.POST)
            context["message"]="Succesfuly loaded flight!"
        elif "add_passager_form" in request.POST:
            data_manager.upload_passager(request.POST)
            context["message"] = "Succesfuly loaded passager"
        else:
            print("Error")
    return render(request, template_name="airline/add_data.html", context=context)
