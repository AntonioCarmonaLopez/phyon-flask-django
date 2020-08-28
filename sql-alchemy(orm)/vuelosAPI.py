from flask import Flask,request
from flask import jsonify
import simplejson
from modelos import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://web:web@localhost/vuelos"
app.config["SQLALCHEMY_TRACKS_MODIFICATIONS"] =  False
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(debug=True, host='0.0.0.0')
app.secret_key = "12345"
'''se vicula BD con esta api'''
db.init_app(app)

@app.errorhandler(404)
def page_not_found(err):
    return render_template("page_not_found.html"), 404
	
@app.route("/api/")
def index():
	vuelos = Vuelo.query.all()
	if vuelos is None:
		return jsonify({"error": "No hay vuelos"}),204
	arrayVuelos = []
	for vuelo in vuelos:
		arrayVuelosTemp = {
			"origen" : vuelo.origen,
			"destino" : vuelo.destino,
			"duracion" : vuelo.duracion
		}
		arrayVuelos.append(arrayVuelosTemp)
	return simplejson.dumps(arrayVuelos)
	
@app.route("/api/reserva", methods=["POST"])
def reserva():
	if request.method == 'POST':
		parametros = {
        	'id_vuelo': request.values.get('id_vuelo')
   		}
		if not parametros['id_vuelo']:
			return jsonify({"error": "Falta id_vuelo(url-encoded)"}),400
		nombre = request.form.get('nombre')
		if not nombre:
			 return jsonify({"error": "Falta nombre pasajero(form-body)"}),405
		vuelo = Vuelo.query.get(parametros['id_vuelo'])
		if not vuelo:
			return jsonify({"error": "id vuelo no valido"}),422
		id = parametros['id_vuelo']+nombre
		vuelo.insertarPasajero(id,nombre)
		return jsonify({"Estado": "Vuelo reservado"}),201
	else:
		return jsonify({"error": "Método incorrecto->post"}),405

@app.route("/api/vuelos/<id_vuelo>")
def vuelo(id_vuelo):	
	vuelo = Vuelo.query.get(id_vuelo)
	if not vuelo:
		return jsonify({"error": "id vuelo no valido"}),422
	pasajeros = vuelo.pasajeros
	nombres = []
	for pasajero in pasajeros:
		nombres.append(pasajero.nombre)
	return jsonify({
		"origen": vuelo.origen,
		"destino": vuelo.destino,
		"duracion": vuelo.duracion,
		"pasajeros": nombres
	})

@app.route("/api/nuevoVuelo",methods=["GET","POST"])
def nuevoVuelo():
	if request.method == 'POST':	
		origen = request.form.get('origen')
		if not origen:
			return jsonify({"error": "Falta Aropuerto origen(form-body)"}),400
		else:
			aero_origen = Aeropuerto.query.get(origen)
			if aero_origen:
				return jsonify({"error": "Aeropuerto origen no existe"}),204
		destino = request.form.get('destino')
		if not destino:
			return jsonify({"error": "Falta Aeropuerto destino(form-body)"}),400
		else:
			aero_destino = Aeropuerto.query.get(destino)
			if aero_destino:
				return jsonify({"error": "Aeropuerto destino no existe"}),204
		duracion = request.form.get('duracion')	
		if not duracion:
			return jsonify({"error": "Falta duración del vuelo(form-body)"}),405	
		
		id = origen+'2'+destino
		newVuelo=Vuelo.query.get(id)
		if newVuelo:
			return jsonify({"error": "id vuelo ya existe"}),204
		vuelo = Vuelo(id=id,origen=origen,destino=destino,duracion=duracion)
		resultado=vuelo.insertarVuelo()
		if resultado:
			return jsonify({"Estado": "Vuelo añadido"}),201
		else:
			return jsonify({"Estado": "Vuelo No añadido"}),202
	elif request.method == 'GET':
		return jsonify({"formulario": "GET"}),200

@app.route("/api/nuevoAeropuerto",methods=["GET","POST"])
def nuevoAeropuerto():	
	if request.method == 'POST':
		codigo = request.form.get("codigo")
		nombre = request.form.get("nombre")
		if not codigo or not nombre:
			if not codigo:
				return jsonify({"error": "Falta código aeropuerto(form-body)"}),400
			elif not nombre:
				return jsonify({"error": "Falta nombre aeropuerto(form-body)"}),400
		else:
			aeropuerto = Aeropuerto(codigo=codigo,nombre=nombre)
			resultado = aeropuerto.insertarAeropuerto()
			if resultado:
				return jsonify({"Estado": "Aeropuerto añadido"}),201
			else:
				return jsonify({"Estado": "Aeropuerto No añadido"}),202
	elif request.method == 'GET':
		return jsonify({"formulario": "GET"}),200

@app.route("/api/login",methods=["GET","POST"])
def login():
	if request.method == 'POST':	
		nombre = request.form.get("nombre")
		password = request.form.get("password")
		if not nombre or not password:
			if not nombre:
				return jsonify({"Error","Falta nombre"})
			elif not password:
				return jsonify({"Error","Falta password"})
		else:
			usuario = Usuario.query.filter_by(nombre=nombre).first()
			if usuario and check_password_hash(usuario.password,password):
				session["usuario"] = usuario.nombre
				flash("Usuario logueado", "success")
				return jsonify("OK","Login correcto"})
			return jsonify("Error","Login incorrecto"})
		return jsonify({"Error","Usuario no logeado, credenciales incorrectas"})
	elif request.method == 'GET':
		return jsonify({"formulario": "GET"}),200

@app.route("/api/logout")
def logout():
    session.pop("username", None)
    return jsonify({"Estado": "Usuario se ha deslogeado"}),200

@app.route("/api/registrar",methods=["GET","POST"])
def registrar():	
	if request.method == 'POST':
		nombre = request.form.get("nombre")
		password = request.form.get("password")
		password2 = request.form.get("password2")
		perfil = 'usuario'
		id = nombre+perfil
		if not nombre or not password or not password2:
			if not nombre:
				return jsonify({"Error": "nombra vacio"}),400
			elif not password:
				return jsonify({"Error": "contraseña vacia"}),400
			elif not password2:
				return jsonify({"Error": "Confirmación contraseña vacia"}),400
		elif len(password) < 9:
			return jsonify({"Error": "contraseña menor de 8 caracteres"}),400
		elif password != password2:
			return jsonify({"Error": "Las contraseñas no coinciden"}),400
		else:
			hashed_pw = generate_password_hash(password, method="sha256")
			usuario = Usuario.query.filter_by(nombre=nombre).first()
			if not usuario:
				usuario = Usuario(id=id,nombre=nombre,password=hashed_pw,perfil=perfil)
				resultado = usuario.crearUsuario()
				if resultado:
					return jsonify({"Estado": "Usuario creado"}),200
			else:
				return jsonify({"Estado": "Usuario no se creo"}),400
			return jsonify({"Estado": "Usuario no se creo"}),400
	

