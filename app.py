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
    if request.method == "POST":
        # parse join/new game
        myMode = request.form.get("mode")
        if myMode == "monitor":
            return redirect(url_for('route_mon'))
        elif myMode == "control":
            return redirect(url_for('route_ctrl'))
        elif myMode == "advance":
            return redirect(url_for('route_adv'))
        else:
            return redirect(url_for('route_index'), code=303)
    else:
        return redirect(url_for('route_index'), code=404)

@app.route("/monitor", methods=["GET"])
def route_mon():
    return redirect(url_for('route_index'), code=404)

@app.route("/control", methods=["GET","POST"])
def route_ctrl():
    if request.method == "POST":
        pass    #TODO
    else:
        return redirect(url_for('route_index'), code=404)

@app.route("/advance", methods=["GET","POST"])
def route_adv():
    if request.method == "POST":
        pass    #TODO
    else:
        return redirect(url_for('route_index'), code=404)
