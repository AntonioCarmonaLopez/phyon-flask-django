from django.contrib import admin
from .models import Vuelo, Aeropuerto, Pasajero

class PasajeroInline(admin.StackedInline):
    model = Pasajero.vuelos.through
    extra = 1

class VueloAdmin(admin.ModelAdmin):
    inlines = [PasajeroInline]

class PasajeroAdmin(admin.ModelAdmin):
    filter_horizontal = ("vuelos",)

admin.site.register(Aeropuerto)
admin.site.register(Vuelo, VueloAdmin)
admin.site.register(Pasajero, PasajeroAdmin)