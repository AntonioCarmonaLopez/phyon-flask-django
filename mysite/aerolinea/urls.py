from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("<int:id_vuelo>",views.vuelo,name="vuelo"),
    path("<int:id_vuelo>/reserva",views.reserva,name="reserva")
]