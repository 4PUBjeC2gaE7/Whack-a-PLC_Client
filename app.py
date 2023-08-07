from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_session import Session
from enum import Enum
from random import randrange, choice
import json

# Configure app
app = Flask(__name__)
app.debug = True

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET","POST"])
def route_index():
    match request.method:
        case "POST":
            # parse join/new game
            match request.form.get("mode"):
                case "monitor":
                    return redirect(url_for('route_mon'))
                case "control":
                    return redirect(url_for('route_ctrl'))
                case "advance":
                    return redirect(url_for('route_adv'))
                case _:
                    return redirect(url_for('route_index'), code=303)
        case "GET":
            return render_template("index.html")
        case _:
            return redirect(url_for('route_index'), code=404)

@app.route("/monitor", methods=["GET"])
def route_mon():
    return redirect(url_for('route_index'), code=404)

@app.route("/control", methods=["GET","POST"])
def route_ctrl():
    match request.method:
        case "POST":
            pass    #TODO
        case "GET":
            pass    #TODO
        case _:
            return redirect(url_for('route_index'), code=404)

@app.route("/advance", methods=["GET","POST"])
def route_adv():
    match request.method:
        case "POST":
            pass    #TODO
        case "GET":
            pass    #TODO
        case _:
            return redirect(url_for('route_index'), code=404)
