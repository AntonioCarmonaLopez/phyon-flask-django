import csv

from flask import Flask,render_template,request
from modelos import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://web:web@localhost/vuelos"
app.config["SQLALCHEMY_TRACKS_MODIFICATIONS"] =  False

archivoVuelos = 'vuelos.csv'
archivoAeropuertos = 'aeropuertos.csv'

'''se vicula BD con esta api'''
db.init_app(app)

def vuelo():
	fv = open(archivoVuelos)
	readerv = csv.reader(fv)
	for id,origen,destino,duracion in readerv:
		vuelo = Vuelo(id=id,origen=origen,destino=destino,duracion=duracion)
		try:
			db.session.add(vuelo)		
			print(f"vuelo con id {id} añadido de {origen} a {destino} y duración {duracion}")
		except Exception as ex:
			print(ex)
	db.session.commit()

def aeropuerto():
	fa = open(archivoAeropuertos)
	readera = csv.reader(f)a
	for codigo,nombre in readera:
		aero = Aerepuerto(codigo=codigo,nombre=nombre)
		try:
			db.session.add(aeç)		
			print(f"Aeropuerto con código {codigo} y {nombre} añadido")
		except Exception as ex:
			print(ex)
	db.session.commit()
if __name__ == "__main__":
    with app.app_context():
        vuelo()
		aeropuerto()
