from django.contrib import admin
from .models import Airport, Flight, Passager, Route


# Register your models here.
class AirportAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "country"]
    list_filter = ["country"]
    exclude = ("longitude", "latitude", "departures", "arrivals")
    search_fields = ["airport_id", "name", "city", "country"]

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

    flight_departures.short_description = "Departures"
    flight_arrival.short_description = "Arrival"
    readonly_fields = ["flight_departures", "flight_arrival"]


class FlightAdmin(admin.ModelAdmin):
    list_display = ["id", "start", "destination", "date"]
    filter_horizontal = ["passengers", "passenger_set"]
    list_filter = ["start", "destination"]
    search_fields = [
        "start__name",
        "start__city",
        "start__country",
        "destination__name",
        "destination__city",
        "destination__country",
        "id",
    ]


class PassagerAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "surname"]
    filter_horizontal = ["flights"]
    search_fields = ["id", "first_name", "surname"]


class RouteAdmin(admin.ModelAdmin):
    list_display = ["id", "start", "destination"]
    exclude = ["date"]


admin.site.register(Airport, AirportAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passager, PassagerAdmin)
admin.site.register(Route, RouteAdmin)
