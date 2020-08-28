from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.shortcuts import HttpResponse,render, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Vuelo, Aeropuerto, Pasajero
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

import logging

# Create your views here.
def error_404_view(request,exception):
    return render(request,'404.html')

@csrf_exempt
def vuelos(request):
    if not request.user.is_authenticated:
        return render(request, "vuelos/index.html", {"msg": "Usuario no logeado-error"})
    else:
        listaVuelos = Vuelo.objects.all()
        page = request.GET.get('page', 1)
        paginador = Paginator(listaVuelos, 1)
        vuelos = paginador.page(page)
        context = {
            "vuelos": vuelos
        }
        return render(request,"vuelos/vuelos.html",context)

def vuelo(request,id_vuelo):
    if not request.user.is_authenticated:
        return render(request, "vuelos/index.html", {"msg": "Usuario no logeado-error"})
    else:
        try:
            vuelo = Vuelo.objects.get(pk=id_vuelo)
        except Vuelo.DoesNotExist:
            raise Http404("El vuelo no existe.error")
        context = {
            "vuelo": vuelo,
            "pasajeros":vuelo.pasajeros.all(),
            "noPasajeros": Pasajero.objects.exclude(vuelos=vuelo)
        }
        return render(request,"vuelos/vuelo.html",context)

def reserva(request,id_vuelo):
    if not request.user.is_authenticated:
        return render(request, "vuelos/index.html", {"msg": "Usuario no logeado-error"})
    else:
        try:
            id_pasajero = int(request.session["pasajero"])
            pasajero = Pasajero.objects.get(pk=id_pasajero)
            vuelo = Vuelo.objects.get(pk=id_vuelo)
        except KeyError:
            return render(request,"vuelos/error.html", {"msg":"no selection-error"})
        except Vuelo.DoesNotExist:
            return render(request,"vuelos/error.html", {"msg":"no hay  vuelos-error"})
        except Pasajero.DoesNotExist:
            return render(request,"vuelos/error.html", {"msg":"no existe el pasajero-error"})
        
        pasajero.vuelos.add(vuelo)
        return HttpResponseRedirect(reverse("vuelo", args=(id_vuelo,)))

def login(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, "vuelos/index.html", {"msg": None})
        else:
            context = {
                "user": request.user
            }
            return render(request, "vuelos/vuelos.html", context)
    elif request.method == 'POST':
        username = request.POST["txtUsuario"]
        password = request.POST["txtPass"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("vuelos"))
        else:
            return render(request, "vuelos/index.html", {"msg": "Credenciales invalidas-error"})

def logout(request):
    auth_logout(request)
    return render(request, "vuelos/index.html", {"msg": "El usuario ha salido-exito"})

def registro(request):	
    if request.user.is_authenticated:
            return render(request, "vuelos/index.html", {"msg": "Existe un usuario activo-error"})
    else:
        if request.method == "GET":    
            return render(request, "vuelos/registro.html")
        elif request.method == "POST":
            usuario = request.POST["usuario"]
            email = request.POST["email"]
            password = request.POST["password"]
            user = User.objects.create_user(username=usuario, email=email, password=password)
            if request.user.is_authenticated:
                logout(request)
            return render(request, "vuelos/index.html", {"msg": "El usuario se ha creado-exito"})