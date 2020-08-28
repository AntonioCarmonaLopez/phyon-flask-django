from django.urls import path

from . import views

urlpatterns = [
    path("",views.login,name="index"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("registro",views.registro,name="registro"),
    path("vuelos",views.vuelos,name="vuelos"),
    path("<int:id_vuelo>",views.vuelo,name="vuelo"),
    path("<int:id_vuelo>/reserva",views.reserva,name="reserva")
]