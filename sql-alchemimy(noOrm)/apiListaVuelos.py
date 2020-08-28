from flask import Flask,render_template,request

'''
importaciones motor alchemy, sesión de ámbitos y creador de sesiones
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
'''
importar clases
'''
from Vuelo import *
from Pasajero import *

app = Flask(__name__)


conn = 'postgresql://web:web@127.0.0.1/vuelos'



vuelosAll= "SELECT* FROM vuelos"


vueloDestino = "SELECT a.nombre FROM vuelos as v\
					INNER JOIN destinos as a ON v.destino_id = a.id\
					WHERE v.id = :id"

insertarPasajero = "INSERT INTO pasajeros(nombre,vuelo_id) VALUES (:nombre,:id_vuelo)"

idVuelo = "SELECT * FROM vuelos\
					WHERE id = :id_vuelo"

pasajerosVuelo = "SELECT* FROM pasajeros\
					WHERE vuelo_id = :id_vuelo"

aeropuertos = "SELECT* FROM aeropuertos"

insertarVuelo = "INSERT INTO vuelos(id,origen,destino,duracion) VALUES (:id,:origen,:destino,:duracion)"

insertarAereopuerto = "INSERT INTO aeropuertos(codigo,nombre) VALUES (:codigo,:nombre)"


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')

try:
	engine = create_engine(conn)
	db = scoped_session(sessionmaker(bind=engine))
except Exception as ex:
	print(ex)

@app.route("/")
def index():
	vuelos = db.execute(vuelosAll).fetchall()
	return render_template("index.html",vuelos=vuelos)

@app.route("/reserva", methods=["POST"])
def reserva():
	nombre = request.form.get("nombre")
	if not nombre:
		return render_template("error.html", msg="Nombre vacio")
	try:
		id_vuelo = request.form.get("id_vuelo")
	except Exception as ex:
		return render_template("error.html", msg=ex)
	if db.execute(idVuelo,{"id_vuelo": id_vuelo}).rowcount == 0:
		return render_template("error.html", msg="id vuelo no valido")
	try:
		db.execute(insertarPasajero,{"nombre": nombre,"id_vuelo": id_vuelo})
		db.commit()
		return render_template("ok.html",nombre=nombre,id_vuelo=id_vuelo)
	except Exception as ex:
		return render_template("error.html", msg=ex)			
		
@app.route("/vuelos")
def vuelos():
	try:
		vuelos = db.execute(vuelosAll).fetchall()
		return render_template("vuelos.html",vuelos=vuelos)
	except Exception as ex:
		return render_template("error.html", msg=ex)

@app.route("/vuelos/<id_vuelo>")
def vuelo(id_vuelo):	
	vuelo = db.execute(idVuelo,{"id_vuelo": id_vuelo}).fetchone()
	if vuelo is None:
		return render_template("error.html", msg="id vuelo no valido")
	else:
		try:
			pasajeros = db.execute(pasajerosVuelo,{"id_vuelo":id_vuelo}).fetchall()
			return render_template("vuelo.html",vuelo=vuelo,pasajeros=pasajeros)
		except Exception as ex:
			return render_template("error.html", msg=ex)

@app.route("/nuevoVuelo")
def nuevoVuelo():	
	try:
		aero = db.execute(aeropuertos).fetchall()
		return render_template("nuevoVuelo.html",aero=aero)
	except Exception as ex:
		return render_template("error.html", msg=ex)

@app.route("/nuevoVuelo",methods=["POST"])
def nuevoVuelo2():	
	id = request.form.get("id")
	origen = request.form.get("origen")
	destino = request.form.get("destino")
	duracion = request.form.get("duracion")
	if not id or not origen or not destino or not duracion:
		if not id:
			return render_template("error.html", msg="id vacio")
		elif not origen:
			return render_template("error.html", msg="origen vacio")
		elif not destino:
			return render_template("error.html", msg="destino vacio")
		elif not duracion:
			return render_template("error.html", msg="duracion vacio")
	else:
		try:
			db.execute(insertarVuelo,{"id":id,"origen":origen,"destino":destino,"duracion":int(duracion)})
			db.commit()
			msg ="Alta correcta del vuelo con origen {{ origen }}, destino {{ destino }} y duración {{ duracion }}"
			return render_template("ok.html",msg)
		except Exception as ex:
			return render_template("error.html", msg=ex)

@app.route("/nuevoAeropuerto")
def nuevoAereopuerto():	
		return render_template("nuevoAereo.html")

@app.route("/nuevoAeropuerto",methods=["POST"])
def nuevoAeropuerto2():	
	codigo = request.form.get("codigo")
	nombre = request.form.get("nombre")
	if not codigo or not nombre:
		if not codigo:
			return render_template("error.html", msg="codigo vacio")
		elif not nombre:
			return render_template("error.html", msg="nombre vacio")
	else:
		try:
			db.execute(insertarAereopuerto,{"codigo":codigo,"nombre":nombre})
			db.commit()
			msg ="Alta correcta del aereopuerto con nombre {{ nombre }} y código {{ codigo }}"
			return render_template("ok.html")
		except Exception as ex:
			return render_template("error.html", msg=ex)
