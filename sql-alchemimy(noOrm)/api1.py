import datetime

from flask import Flask,render_template

app=Flask(__name__)

@app.route("/")
def index():
	ahora=datetime.datetime.now()
	nAnyo=ahora.month==1 and ahora.day==1
	return render_template("index.html",nAnyo=nAnyo)
