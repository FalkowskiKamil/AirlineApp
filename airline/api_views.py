import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from airline.models import Airport, Flight, Route, Passager, FlightPassager

def airport_to_dict(airport):
    return {
        "pk": airport.pk,
        "name": airport.name,
        "city": airport.city,
        "country": airport.country,
        "latitude": airport.latitude,
        "longitude": airport.longitude,
    }

@csrf_exempt
def airport_list(request):
    if request.method == "GET":
        airports = Airport.objects.all()
        airports_as_dict = [airport_to_dict(a) for a in airports]
        return JsonResponse({"data": airports_as_dict})
    elif request.method == "POST":
        airport_data = json.loads(request.body)
        airport = Airport.objects.create(**airport_data)
        return HttpResponse(
            status = HTTPStatus.CREATED,
            headers = {"Location": reverse("api_airport_detail", args=(airport.pk, ))},
        )
    return HttpResponseNotAllowed(["GET", "POST"])

@csrf_exempt
def airport_detail(request, pk):
    airport = get_object_or_404(Airport, pk = pk)
    if request.method == "GET":
        return JsonResponse(airport_to_dict(airport))
    elif request.method == "PUT":
        airport_data = json.loads(request.body)
        for field, value in airport_data.items():
            setattr(airport, field, value)
        airport.save()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    elif request.method == "DELETE":
        airport.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])