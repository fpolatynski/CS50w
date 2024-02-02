from django.contrib import admin

from .models import Airport, Flight, Passengers


class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin","destination", "duration")


class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights", )


admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passengers, PassengerAdmin)
