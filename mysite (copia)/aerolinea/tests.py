from django.db.models import Max
from django.test import Client, TestCase

from .models import Aeropuerto, Vuelo, Pasajero

# Create your tests here.
class VuelosTestCase(TestCase):

    def setUp(self):

        # Create airports.
        a1 = Aeropuerto.objects.create(codigo="AAA", ciudad="City A")
        a2 = Aeropuerto.objects.create(codigo="BBB", ciudad="City B")

        # Create flights.
        Vuelo.objects.create(origen=a1, destino=a2, duracion=100)
        Vuelo.objects.create(origen=a1, destino=a1, duracion=200)

    def test_salidas_count(self):
        a = Aeropuerto.objects.get(codigo="AAA")
        self.assertEqual(a.salidas.count(), 2)

    def test_llegadas_count(self):
        a = Aeropuerto.objects.get(codigo="AAA")
        self.assertEqual(a.llegadas.count(), 1)

    def test_valid_vuelo(self):
        a1 = Aeropuerto.objects.get(codigo="AAA")
        a2 = Aeropuerto.objects.get(codigo="BBB")
        v = Vuelo.objects.get(origen=a1, destino=a2)
        self.assertTrue(v.esValido())

    def test_invalid_vuelo_destino(self):
        a1 = Aeropuerto.objects.get(codigo="AAA")
        v = Vuelo.objects.get(origen=a1, destino=a1)
        self.assertFalse(v.esValido())

    def test_invalid_flight_duracion(self):
        a1 = Aeropuerto.objects.get(codigo="AAA")
        a2 = Aeropuerto.objects.get(codigo="BBB")
        v = Vuelo.objects.get(origen=a1, destino=a2)
        v.duracion = -100
        self.assertFalse(v.esValido())

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["vuelos"].count(), 2)

    def test_valid_vuelo_page(self):
        a1 = Aeropuerto.objects.get(codigo="AAA")
        v = Vuelo.objects.get(origen=a1, destino=a1)

        c = Client()
        response = c.get(f"/{v.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_vuelo_page(self):
        max_id = Vuelo.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_vuelo_page_pasajero(self):
        v = Vuelo.objects.get(pk=1)
        p = Pasajero.objects.create(nombre="Alice", apellido="Adams")
        v.pasajeros.add(p)

        c = Client()
        response = c.get(f"/{v.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["pasajeros"].count(), 1)

    def test_vuelo_page_no_pasajeros(self):
        v = Vuelo.objects.get(pk=1)
        p = Pasajero.objects.create(nombre="Alice", apellido="Adams")

        c = Client()