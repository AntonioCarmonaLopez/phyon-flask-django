from flask import Flask,render_template,request
from modelos import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://web:web@localhost/articulos"
app.config["SQLALCHEMY_TRACKS_MODIFICATIONS"] =  False
'''se vicula BD con esta api'''
db.init_app(app)

def main():
    '''crea las tablas desde modelos'''
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()