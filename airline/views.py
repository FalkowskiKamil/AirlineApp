from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from folium import Map
from airline.models import Airport, Flight, Route, Passager
from utils import data_manager
from utils.mongo_connection import connect_to_mongodb
from utils.map_creator import create_full_map, create_map


# Create your views here.
def main(request: HttpRequest) -> HttpResponse:
    countries: list[str] = list(Airport.objects.values_list("country", flat=True).distinct())
    context: dict = {
        "countries": countries,
    }
    return render(request, template_name="airline/main.html", context=context)


def country_map(request: HttpRequest) -> HttpResponse:
    context: dict = {}
    if request.method == "POST":
        if not request.POST["destination_country"]:
            route: list[Route] = list(Route.objects.filter(# type:ignore
                start__country=request.POST["start_country"].title()
            )) 
        else:
            route: list[Route] = list(Route.objects.filter(
                start__country=request.POST["start_country"].title(),
                destination__country=request.POST["destination_country"].title(),
            ))
        if route:
            map: Map = create_full_map(route)
            context: dict = {"map": map._repr_html_()}
    return render(request, template_name="airline/full_map.html", context=context)


def airport(request: HttpRequest, airport_id) -> HttpResponse:
    airport: object = get_object_or_404(Airport, pk=airport_id)
    map: Map = create_map(airport)
    context: dict = {
        "airport": airport,
        "map": map._repr_html_(),
        "countries": Airport.objects.values_list("country", flat=True).distinct(),
    }
    return render(request, template_name="airline/airport.html", context=context)


def routes(request: HttpRequest, route_id: int) -> HttpResponse:
    route: object = get_object_or_404(Route, pk=route_id)
    map: Map = create_map(route.start, route.destination)
    context: dict = {"route": route, "map": map._repr_html_()}
    return render(request, template_name="airline/route.html", context=context)


def flight(request: HttpRequest, fli_id: int) -> HttpResponse:
    flight: object = get_object_or_404(Flight, pk=fli_id)
    map: Map = create_map(flight.start, flight.destination)
    context: dict = {"flight": flight, "map": map._repr_html_()}
    if request.method == "POST":
        data_manager.sign_for_flight(request.user.passager_user.first().id, fli_id) # type: ignore
        messages.success(request, message=f"Succesfuly signed for flight {flight.id}") # type: ignore
    return render(request, template_name="airline/flight.html", context=context)


def passager(request: HttpRequest, passager_id) -> HttpResponse:
    passager: object = get_object_or_404(Passager, pk=passager_id)
    context: dict = {
        "passager": passager,
        "countries": Airport.objects.values_list("country", flat=True).distinct(),
    }
    return render(request, template_name="airline/passager.html", context=context)


def full_map(request: HttpRequest) -> HttpResponse:
    route: object = Route.objects.all()
    map: Map = create_full_map(route) # type: ignore
    context: dict = {"map": map._repr_html_()}
    return render(request, template_name="airline/full_map.html", context=context)


def full_data_user(request: HttpRequest) -> HttpResponse:
    countries: list[Airport] = list(Airport.objects.values_list("country", flat=True).distinct())
    context: dict = {"countries": countries, "routes": Route.objects.all()}
    return render(request, template_name="airline/full_data_user.html", context=context)


def full_data_staff(request: HttpRequest) -> HttpResponse:
    countries: list[Airport] = list(Airport.objects.values_list("country", flat=True).distinct())
    context: dict = {
        "airport": Airport.objects.all(),
        "passager": Passager.objects.all(),
        "flight": Flight.objects.all().order_by("date"),
        "countries": countries,
    }
    return render(
        request, template_name="airline/full_data_staff.html", context=context
    )


def add_data(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if "add_airport_form" in request.POST:
            message: str = data_manager.upload_airport(request.POST) # type: ignore
        elif "add_flight_form" in request.POST:
            message: str = data_manager.upload_flight(request.POST) # type: ignore
        elif "add_passager_form" in request.POST:
            message: str = data_manager.upload_passager(request.POST) # type: ignore
        elif "add_route_form" in request.POST:
            message: str = data_manager.upload_route(request.POST) # type: ignore
        else:
            messages.error(request, "Something went wrong!")
        messages.success(request, str(f"{message}")) #type: ignore
        return redirect(reverse("airline:add_data"))
    status_of_connection: list = connect_to_mongodb() # type: ignore
    db: df = status_of_connection[1] #type: ignore
    countries: list = list(sorted(db["Country"].unique()))
    flights_already_made: list[Flight] = list(Flight.objects.all())
    routes_alredy_made: list[Route] = list(Route.objects.all())
    airport_alredy_made: list[Airport] = list(Airport.objects.all())
    context: dict = {
        "flights": flights_already_made,
        "routes": routes_alredy_made,
        "airports": airport_alredy_made,
        "countries": countries,
    }
    messages.info(request, str(f"{status_of_connection[0]}")) #type: ignore
    return render(request, template_name="airline/add_data.html", context=context)
