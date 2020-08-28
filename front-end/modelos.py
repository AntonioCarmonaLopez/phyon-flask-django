from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Articulo(db.Model):
    __tablename__ = "articulos"
    id = db.Column(db.String, primary_key=True)
    titulo = db.Column(db.String,nullable = False)
    cuerpo = db.Column(db.String,nullable = False)
    autor = db.Column(db.String,nullable = False)
  
    def __init__(self,id,titulo,cuerpo,autor):
        self.id = id
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.autor = autor

