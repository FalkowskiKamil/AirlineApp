from rest_framework import viewsets

from airline.api.permissions import IsAdminUserForObject
from airline.api.serializers import AirportSerializer, FlightSerializzer, PassagerSerializzer, RouteSerializer
from airline.models import Airport, Flight, Passager, Route


class AirportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserForObject]
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filterset_fields = ["country", "departures", "arrivals"]

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return AirportSerializer


class FlightsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserForObject]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializzer
    filterset_fields = ["start", "destination", "date"]

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return FlightSerializzer

class PassagersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserForObject]
    queryset = Passager.objects.all()
    serializer_class = PassagerSerializzer
    filterset_fields = ["first_name", "surname", "flights"]

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PassagerSerializzer
        
class RoutesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserForObject]
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filterset_fields = ["start", "destination", "flights"] 

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return RouteSerializer
