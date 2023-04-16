from django.contrib import admin
from .models import Airport, Flight, Passager

# Register your models here.
class AirportAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country']
    list_filter = ['country']
    exclude = ('longitude', 'latitude', 'departures', 'arrivals')
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def flight_departures(self, obj):
        flights = Flight.objects.filter(start=obj)
        return ", ".join([str(flight) for flight in flights])
    
    def flight_arrival(self, obj):
        flights2 = Flight.objects.filter(destination=obj)
        return ", ".join([str(flight) for flight in flights2])

    flight_departures.short_description = 'Departures'
    flight_arrival.short_description = 'Arrival'
    readonly_fields = ['flight_departures','flight_arrival']
    
class FlightAdmin(admin.ModelAdmin):
    list_display = ['id', 'start', 'destination', 'date']
    list_filter = ['start', 'destination' ]
    search_fields=['start', 'destination']

class PassagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'surname']
    filter_horizontal = ['flights']



admin.site.register(Airport, AirportAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passager, PassagerAdmin)