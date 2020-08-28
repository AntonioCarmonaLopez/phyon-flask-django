from django.shortcuts import HttpResponse,render, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Vuelo, Aeropuerto, Pasajero
# Create your views here.
def index(request):
    context = {
        "vuelos": Vuelo.objects.all()
    }
    return render(request,"vuelos/index.html",context)

def vuelo(request,id_vuelo):
    try:
        vuelo = Vuelo.objects.get(pk=id_vuelo)
    except Vuelo.DoesNotExist:
        raise Http404("El vuelo no existe")
    context = {
        "vuelo": vuelo,
        "pasajeros":vuelo.pasajeros.all(),
        "noPasajeros": Pasajero.objects.exclude(vuelos=vuelo)
    }
    return render(request,"vuelos/vuelo.html",context)

def reserva(request,id_vuelo):
    try:
        id_pasajero = int(request.POST["pasajero"])
        pasajero = Pasajero.objects.get(pk=id_pasajero)
        vuelo = Vuelo.objects.get(pk=id_vuelo)
    except KeyError:
        return render(request,"vuelos/error.html", {"msg":"no selection"})
    except Vuelo.DoesNotExist:
        return render(request,"vuelos/error.html", {"msg":"no hay  vuelos"})
    except Pasajero.DoesNotExist:
        return render(request,"vuelos/error.html", {"msg":"no existe el pasajero"})
    
    pasajero.vuelos.add(vuelo)
    return HttpResponseRedirect(reverse("vuelo", args=(id_vuelo,)))