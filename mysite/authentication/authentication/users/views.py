from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"msg": None})
    context = {
        "user": request.user
    }
    return render(request, "users/user.html", context)


def login(request):
    usuario = request.POST.get["usuario"]
    password = request.POST.get["password"]
    user = authenticate(request, usuario=usuario, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"msg": "Credenciales invalidas"})

def logout(request):
    logout(request)
    return render(request, "users/login.html", {"msg": "El usuario ha salido"})
