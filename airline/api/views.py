from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from airline.api.permissions import IsAdminUserForObject
from airline.api.serializers import AirportSerializer
from airline.models import Airport

class AirportList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class AirportDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserForObject]
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer