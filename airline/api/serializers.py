from rest_framework import serializers

from airline.models import Airport, Flight, Route, Passager

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"
        readonly = ["latitude", "longitude"]

class FlightSerializzer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["id", "date", "start", "destination"]

class PassagerSerializzer(serializers.ModelSerializer):
    class Meta:
        model = Passager
        fields = "__all__"

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"