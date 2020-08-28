from django.db import models

# Create your models here.
class Aeropuerto(models.Model):
    codigo = models.CharField(max_length=3)
    ciudad = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.codigo} - {self.ciudad}"
class Vuelo(models.Model):
    origen = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE,related_name="salidas")
    destino = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE,related_name="llegadas")
    duracion = models.IntegerField()

    def esValido(self):
        return (self.origen != self.destino) and (self.duracion >= 0)

    def __str__(self):
        return f"{self.id} - {self.origen} a {self.destino}"

class Pasajero(models.Model):
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    vuelos = models.ManyToManyField(Vuelo, blank=True, related_name="pasajeros")

    def __str__(self):
        return f"{self.nombre} - {self.apellido}"