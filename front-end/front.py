from modelos import *

from flask import Flask, render_template

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://web:web@localhost/articulos"
app.config["SQLALCHEMY_TRACKS_MODIFICATIONS"] =  False
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
if __name__ == "__main__":  
    app.run(debug=True, host='0.0.0.0')
app.secret_key = "12345"
'''se vicula BD con esta api'''
db.init_app(app)

@app.errorhandler(404)
def page_not_found(err):
    return render_template("page_not_found.html"), 404

@app.route("/")
def index():
    articulos = Articulo.query.all()
    return render_template("layout.html",articulos=articulos), 200

@app.route("/articulo/<string:id>")
def articulo(id=1):
    art = Articulo.query.get(id)
    return render_template("layout.html",art=art), 200