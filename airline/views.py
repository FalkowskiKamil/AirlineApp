from django.shortcuts import render, get_object_or_404, redirect
from .models import Airport, Flight, Route, Passager
from . import data_manager, map_creator
from user.forms import MessageForm
from django.contrib.auth.models import User
from manage import configure_logger

logger = configure_logger()


# Create your views here.
def main(request):
    """
    Renders the main page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered page.

    """
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {
        "countries": countries,
    }
    return render(request, template_name="airline/main.html", context=context)

def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = User.objects.get(is_superuser=True)
            message.save()

            return redirect('user:message', user_id=request.user.id)

def country(request):
    """
    Renders the page for a searched country.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered page.

    """
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


def all(request):
    """
    Renders the page with all routes.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered page.

    """
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {"countries": countries, "routes": Route.objects.all()}
    return render(request, template_name="airline/all.html", context=context)


def staff(request):
    """
    Renders the staff page with all of the data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered page.

    """
    countries = Airport.objects.values_list("country", flat=True).distinct()
    context = {
        "airport": Airport.objects.all(),
        "passager": Passager.objects.all(),
        "flight": Flight.objects.all().order_by("date"),
        "countries": countries,
    }
    return render(request, template_name="airline/main_staff.html", context=context)


def passager(request, passager_id):
    """
    Renders the page for a specific passenger.

    Args:
        request (HttpRequest): The HTTP request object.
        passager_id (int): The ID of the passenger.

    Returns:
        HttpResponse: The HTTP response containing the rendered page.

    """
    passager = get_object_or_404(Passager, pk=passager_id)
    context = {
        "passager": passager,
        "countries": Airport.objects.values_list("country", flat=True).distinct(),
    }
    return render(request, template_name="airline/passager.html", context=context)


def flight(request, fli_id):
    """
    Renders the page for a specific flight.

    Args:
        request (HttpRequest): The HTTP request object.
        fli_id (int): The ID of the flight.

    Returns:
        HttpResponse: The HTTP response containing the rendered page.

    """
    flight = get_object_or_404(Flight, pk=fli_id)
    map = map_creator.create_map(flight.start, flight.destination)
    form = MessageForm(initial={"context":f"I would like to check out from my upcoming flight nr: {fli_id}"})
    context = {"flight": flight, "map": map._repr_html_(), "form": form}
    if request.method == "POST":
        data_manager.sign_for_flight(request.user.passager_user.first().id, fli_id)
        context["message"] = "Signed up for flight!"
    return render(request, template_name="airline/flight.html", context=context)


def airport(request, airport_id):
    """
    Renders the page for a specific airport.

    Args:
        request (HttpRequest): The HTTP request object.
        airport_id (int): The ID of the airport.

    Returns:
        HttpResponse: The HTTP response containing the rendered page.

    """
    airport = get_object_or_404(Airport, pk=airport_id)
    map = map_creator.create_map(airport)
    context = {
        "airport": airport,
        "map": map._repr_html_(),
        "countries": Airport.objects.values_list("country", flat=True).distinct(),
    }
    return render(request, template_name="airline/airport.html", context=context)


def routes(request, route_id):
    """
    Renders the page for a specific route.

    Args:
        request (HttpRequest): The HTTP request object.
        route_id (int): The ID of the route.

    Returns:
        HttpResponse: The HTTP response containing the rendered page.

    """
    route = get_object_or_404(Route, pk=route_id)
    map = map_creator.create_map(route.start, route.destination)
    context = {"route": route, "map": map._repr_html_()}
    return render(request, template_name="airline/route.html", context=context)


def add_data(request):
    """
    Renders the page for adding data to the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered page.

    """
    context = {}
    if request.method == "POST":
        match list(request.POST.keys())[1]:
            case "airport":
                data_manager.upload_airport(request.POST)
                logger.info(f"Added {request.POST.get('airport')} airport")
                context = {"message": "Succesfuly loaded airport!"}
            case "flight":
                data_manager.upload_flight(request.POST)
                logger.info(f"Added {request.POST.get('flight')} flight")
                context = {"message": "Succesfuly loaded flight!"}
            case "passager":
                data_manager.upload_passager(request.POST)
                logger.info(f"Added {request.POST.get('passager')} passager")
                context = {"message": "Succesfuly loaded passager"}
    return render(request, template_name="airline/add_data.html", context=context)
