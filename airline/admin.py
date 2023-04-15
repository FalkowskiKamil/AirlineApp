from django.contrib import admin
from .models import Airport, Flight, Passager

# Register your models here.

class AirportAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'code']


class FlightAdmin(admin.ModelAdmin):
    list_display = ['id', 'flight_number']
    list_filter = ['start', 'destination', 'date']

class PassagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'surname']
    filter_horizontal = ['flights']





admin.site.register(Airport, AirportAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passager, PassagerAdmin)