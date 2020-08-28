from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vuelo(db.Model):
    __tablename__ = "vuelos"
    id = db.Column(db.String, primary_key=True)
    origen = db.Column(db.String, nullable=False)
    destino = db.Column(db.String, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    pasajeros = db.relationship("Pasajero",backref="vuelo",lazy=True)

    def __init__(self,id,origen,destino,duracion):
        self.id = id
        self.origen = origen
        self.destino = destino
        self.duracion = duracion
    
    def insertarPasajero(self,id,nombre):
        pasajero = Pasajero(id=id,nombre=nombre,vuelo_id=self.id)
        db.session.add(pasajero)
        db.session.commit()

    def insertarVuelo(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

class Pasajero(db.Model):
    __tablename__ = "pasajeros"
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    vuelo_id = db.Column(db.String,db.ForeignKey("vuelos.id"), nullable=False)

class Aeropuerto(db.Model):
    __tablename__ = "aeropuertos"
    codigo = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)

    def __init__(self,codigo,nombre):
        self.codigo = codigo
        self.nombre = nombre

    def insertarAeropuerto(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String(80), unique=True)
    password = db.Column(db.String, nullable=False)
    perfil = db.Column(db.String, nullable=False)
    
    def __init__(self, id,nombre, password,perfil):
        self.id = id
        self.nombre = nombre
        self.password = password
        self.perfil = perfil
        
    def crearUsuario(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False