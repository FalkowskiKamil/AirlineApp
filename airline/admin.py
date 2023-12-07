from django.contrib import admin
from .models import Airport, Flight, Passager, Route, FlightPassager


# Register your models here.
class AirportAdmin(admin.ModelAdmin):
    list_display: list[str]= ["name", "city", "country"]
    list_filter: list[str]= ["country"]
    exclude: tuple = ("longitude", "latitude", "departures", "arrivals")
    search_fields: list[str]= ["airport_id", "name", "city", "country"]

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def flight_departures(self, obj: object) -> str:
        flights = Flight.objects.filter(start=obj)
        return ", ".join([str(flight) for flight in flights])

    def flight_arrival(self, obj: object) -> str:
        flights2 = Flight.objects.filter(destination=obj)
        return ", ".join([str(flight) for flight in flights2])

    flight_departures.short_description = "Departures"
    flight_arrival.short_description = "Arrival"
    readonly_fields: list[str]= ["flight_departures", "flight_arrival"]


class FlightAdmin(admin.ModelAdmin):
    list_display: list[str]= [
        "id",
        "start",
        "destination",
        "date",
        "number_routes",
        "get_passager_flight",
    ]
    list_filter: list[str]= ["start", "destination"]
    search_fields: list[str]= [
        "start__name",
        "start__city",
        "start__country",
        "destination__name",
        "destination__city",
        "destination__country",
        "id",
    ]

    def number_routes(self, obj) -> str:
        return ", ".join(str(route) for route in obj.routes.all())

    def get_passager_flight(self, obj: Flight) -> str:
        if obj.passengers_flights.exists():
            return ", ".join(
                [f"{passager.id}" for passager in obj.passengers_flights.all()]
            )
        else:
            return "None"

    get_passager_flight.short_description = "Id of Passagers"

    class PassengerInline(admin.TabularInline):
        model: Airport = Flight.passengers_flights.through
        extra = 1

    inlines: list= [PassengerInline]


class PassagerAdmin(admin.ModelAdmin):
    list_display: list[str]= ["id", "first_name", "surname", "get_flight_passager"]
    search_fields: list[str]= ["id", "first_name", "surname"]

    def get_flight_passager(self, obj: Passager) -> str:
        if obj.flights.exists():
            return ", ".join([f"{flight.id}" for flight in obj.flights.all()])
        else:
            return "None"

    get_flight_passager.short_description = "Registered Flight"

    class FlightInline(admin.TabularInline):
        model: Airport = Passager.flights.through
        extra = 1

    inlines = [FlightInline]


class RouteAdmin(admin.ModelAdmin):
    list_display: list[str] = ["id", "start", "destination"]
    exclude: list[str] = ["date"]


admin.site.register(Airport, AirportAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passager, PassagerAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(FlightPassager)
