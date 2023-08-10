from django.contrib import admin

from .models import (
    ShowSession,
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    Reservation,
    Ticket
)

admin.site.register(ShowSession)
admin.site.register(ShowTheme)
admin.site.register(AstronomyShow)
admin.site.register(PlanetariumDome)
admin.site.register(Reservation)
admin.site.register(Ticket)

