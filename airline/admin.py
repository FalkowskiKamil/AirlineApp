from django.contrib import admin
from .models import Airport, Flight, Passager, Route, FlightPassager


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
    list_display = [
        "id",
        "start",
        "destination",
        "date",
        "number_routes",
        "get_passager_flight",
    ]
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

    def number_routes(self, obj):
        return ", ".join(str(route) for route in obj.routes.all())

    def get_passager_flight(self, obj):
        if obj.passengers_flights.exists():
            return ", ".join(
                [f"{passager.id}" for passager in obj.passengers_flights.all()]
            )
        else:
            return "None"

    get_passager_flight.short_description = "Id of Passagers"

    class PassengerInline(admin.TabularInline):
        model = Flight.passengers_flights.through
        extra = 1

    inlines = [PassengerInline]


class PassagerAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "surname", "get_flight_passager"]
    search_fields = ["id", "first_name", "surname"]

    def get_flight_passager(self, obj):
        if obj.flights.exists():
            return ", ".join([f"{flight.id}" for flight in obj.flights.all()])
        else:
            return "None"

    get_flight_passager.short_description = "Registered Flight"

    class FlightInline(admin.TabularInline):
        model = Passager.flights.through
        extra = 1

    inlines = [FlightInline]


class RouteAdmin(admin.ModelAdmin):
    list_display = ["id", "start", "destination"]
    exclude = ["date"]


admin.site.register(Airport, AirportAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passager, PassagerAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(FlightPassager)
