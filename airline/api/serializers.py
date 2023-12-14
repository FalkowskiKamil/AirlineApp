from rest_framework import serializers
from airline.models import Airport

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"
        readonly = ["latitude", "longitude"]