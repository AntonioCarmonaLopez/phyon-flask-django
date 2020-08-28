from flask import Flask,render_template,request,session,escape,url_for,redirect,flash
from werkzeug.security import generate_password_hash,check_password_hash
from modelos import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://web:web@localhost/vuelos"
app.config["SQLALCHEMY_TRACKS_MODIFICATIONS"] =  False
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


app.secret_key = "12345"
'''se vicula BD con esta api'''
db.init_app(app)

@app.errorhandler(404)
def page_not_found(err):
    return render_template("page_not_found.html"), 404
	
@app.route("/")
def index():
	vuelos = Vuelo.query.all()
	return render_template("index.html",vuelos=vuelos)

	
@app.route("/reserva", methods=["POST"])
def reserva():
	nombre = request.form.get("nombre")
	if not nombre:
		flash("Nombre vacio","error")
		return redirect(url_for("reserva"))
	try:
		id_vuelo = request.form.get("id_vuelo")
	except Exception as ex:
		flash(ex,"error")
		return redirect(url_for("index"))
	vuelo = Vuelo.query.get(id_vuelo)
	if not vuelo:
		flash("id vuelo no valido","error")
		return redirect(url_for("reserva"))
	try:
		id = id_vuelo+nombre
		try:
			vuelo.insertarPasajero(id,nombre)
			flash("reserva realizada","success")
			return redirect(url_for("index"))
		except Exception as ex:
			flash(ex,"error")
			return redirect(url_for("index"))
	except Exception as ex:
		flash(ex,"error")
		return redirect(url_for("index"))

@app.route("/vuelos")
def vuelos():
	vuelos = Vuelo.query.all()
	return render_template("vuelos.html",vuelos=vuelos)

@app.route("/vuelos/<id_vuelo>")
def vuelo(id_vuelo):
	perfil = session["rol"]
	if perfil == "admin":	
		vuelo = Vuelo.query.get(id_vuelo)
		if vuelo is None:
			flash("id vuelo no valido","error")
			return redirect(url_for("reserva"))
		else:
			try:
				'''
				pasajeros = Pasajero.query.filter_by(vuelo_id=id_vuelo).all()
				'''
				pasajeros = vuelo.pasajeros
				return render_template("vuelo.html",vuelo=vuelo,pasajeros=pasajeros)
			except Exception as ex:
				flash(ex,"error")
				return redirect(url_for("vuelos"))
	flash("No tienes permisos","error")
	return redirect(url_for("index"))

@app.route("/nuevoVuelo",methods=['GET', 'POST'])
def nuevoVuelo():	
	perfil = session["rol"]
	if perfil == "admin":
		if request.method == 'GET':
			try:
				aero = Aeropuerto.query.all()
				return render_template("nuevoVuelo.html",aero=aero)
			except Exception as ex:
				flash("id vuelo no valido","error")
				return redirect(url_for("vuelos"))
		elif request.method == 'POST':
			id = request.form.get("id")
			origen = request.form.get("origen")
			destino = request.form.get("destino")
			duracion = request.form.get("duracion")
			if not id or not origen or not destino or not duracion:
				if not id:
					flash("id vuelo vacio","error")
					return redirect(url_for("nuevoVuelo"))
				elif not origen:
					flash("origen vacio","error")
					return redirect(url_for("nuevoVuelo"))
				elif not destino:
					flash("destino vacio","error")
					return redirect(url_for("nuevoVuelo"))
				elif not duracion:
					flash("duración vuelo vacio","error")
					return redirect(url_for("nuevoVuelo"))
			else:
				vuelo = Vuelo(id=id,origen=origen,destino=destino,duracion=duracion)
				try:
					db.session.add(vuelo)
					db.session.commit()
					flash("Alta correcta del vuelo","success")
					return redirect(url_for("index"))
				except Exception as ex:
					flash("Ya existe un vuelo con este id", "error")
					return redirect(url_for("index"))
	flash("No tienes permisos","error")
	return redirect(url_for("index"))

@app.route("/nuevoAeropuerto",methods=['GET', 'POST'])
def nuevoAeropuerto():
	perfil = session["rol"]
	if perfil == "admin":
		if request.method == 'POST':	
			codigo = request.form.get("codigo")
			nombre = request.form.get("nombre")
			if not codigo or not nombre:
				if not codigo:
					flash("codigo vacio","error")
					return redirect(url_for("nuevoAeropuerto"))
				elif not nombre:
					flash("nombre vacio")
					return redirect(url_for("nuevoAeropuerto"))
			else:
				try:
					aeropuerto = Aeropuerto(codigo=codigo,nombre=nombre)
					db.session.add(aeropuerto)
					db.session.commit()
					flash("Alta correcta del aeropuerto","success")
					return redirect(url_for("index"))
				except Exception as ex:
					flash("Ya existe un aeropuerto con este codigo","error")
					return redirect(url_for("nuevoAeropuerto"))
		return render_template("nuevoAereo.html")
	flash("No tienes permisos","error")
	return redirect(url_for("index"))

@app.route("/actualizar",methods=["POST"])
def actualizar():
	perfil = session["rol"]
	if perfil == "admin":
		if request.method == 'POST':
			origen = request.form.get("origen")
			destino = request.form.get("destino")
			duracion = request.form.get("duracion")
			vueloInfo = Vuelo.query.filter_by(origen=origen,destino=destino).first()
			vuelo = Vuelo.query.get(vueloInfo.id)
			vuelo.origen = origen
			vuelo.destino = destino
			vuelo.duracion = int(duracion)
			db.session.commit()
			flash("Vuelo actualizado","success")
			return redirect(url_for('vuelo', id_vuelo=vuelo.id))
	flash("No tienes permisos","error")
	return redirect(url_for("index"))

@app.route("/borrar/<id_vuelo>")
def borrar(id_vuelo):
	perfil = session["rol"]
	if perfil == "admin":
		vuelo = Vuelo.query.get(id_vuelo)
		db.session.delete(vuelo)
		db.session.commit()
		flash("Vuelo borrado","success")
		return render_template("vuelo.html")
	flash("No tienes permisos","error")
	return redirect(url_for("index"))		

@app.route("/login",methods=["GET","POST"])
def login():
	if request.method == 'POST':	
		nombre = request.form.get("nombre")
		password = request.form.get("password")
		if not nombre or not password:
			if not nombre:
				return redirect(url_for("login"))
			elif not password:
				return redirect(url_for("login"))
		else:
			usuario = Usuario.query.filter_by(nombre=nombre).first()
			if usuario and check_password_hash(usuario.password,password):
				session["usuario"] = usuario.nombre
				session["rol"] = usuario.perfil
				flash("Usuario logueado", "success")
				return redirect(url_for("index"))
			flash("Usuario no logeado","error")
			return redirect(url_for("login"))
		flash("Usuario no logeado, credenciales incorrectas","error")
		return redirect(url_for("login"))
	return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))

@app.route("/registrar",methods=["GET","POST"])
def registrar():	
	if request.method == 'POST':
		nombre = request.form.get("nombre")
		password = request.form.get("password")
		password2 = request.form.get("password2")
		perfil = 'usuario'
		id = nombre+perfil
		if not nombre or not password or not password2:
			if not nombre:
				return redirect(url_for("registrar"))
			elif not password:
				return redirect(url_for("registrar"))
			elif len(password) < 9:
				return redirect(url_for("registrar"))
			elif not password2:
				return redirect(url_for("registrar"))
		elif password != password2:
			return redirect(url_for("registrar"))
		else:
			hashed_pw = generate_password_hash(password, method="sha256")
			usuario = Usuario.query.filter_by(nombre=nombre).first()
			if not usuario:
				usuario = Usuario(id=id,nombre=nombre,password=hashed_pw,perfil=perfil)
				resultado = usuario.crearUsuario()
				if resultado:
					return "Usuario creado"
			else:
				return "Usuario no se creo"
			return "Usuario no se creo"
	return render_template("logup.html")
'''se arranca el servidor'''
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')