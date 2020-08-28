import time,subprocess

from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

salas = ["sala 1", "sala 2"]

@application.before_request
def session_management():
  session.permanent = True

@app.route('/',methods=["GET","POST"])
def index():
    if request.method == 'POST':
        usuario = request.form.get("usuario")
        sala = request.form.get("sala")
        if not usuario:
            return render_template('loginChat.html',salas=salas)
        join_room(sala)
        send({"msg": usuario + " se ha unido a " + sala + " sala."}, sala=sala)
        return render_template('indexSocket2.html')
    return render_template("loginChat.html",salas=salas)

@socketio.on('message')
def handleMessage(datos):
    msg = datos["msg"]
    usuario = datos["usuario"]
    sala = datos["sala"]
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send(msg+' '+time_stamp, broadcast = True)
    send({"usuario": usuario, "msg": msg, "time_stamp": time_stamp}, sala=sala)

if __name__ == '__main__':
    socketio.run(app)
