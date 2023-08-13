from __future__ import division
from flask import Flask, Response, render_template, request, redirect, send_from_directory, url_for, session, abort
from flask_session import Session
from enum import Enum
from random import randrange, choice, gauss
from os import path
import itertools
import threading
import time
import json

# Configure app
app = Flask(__name__)
app.debug = True

#region Test
# Generate streaming data and calculate statistics from it
class MyStreamMonitor(object):
    def __init__(self):
        self.sum   = 0
        self.count = 0
    @property
    def mu(self):
        try:
            outv = self.sum/self.count
        except:
            outv = 0
        return outv
    def generate_values(self):
        while True:
            time.sleep(.1)  # an artificial delay
            yield gauss(0,1)
    def monitor(self, report_interval=1):
        print('Starting data stream...')
        for x in self.generate_values():
            self.sum   += x
            self.count += 1 
#endregion

stream = MyStreamMonitor()

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET","POST"])
def route_index():
    match request.method:
        case "POST":
            # parse join/new game
            match request.form.get("access"):
                case "monitor":
                    return redirect(url_for('route_mon'))
                case "control":
                    return redirect(url_for('route_ctrl'))
                case "advance":
                    return redirect(url_for('route_adv'))
                case _:
                    return redirect(url_for('route_index'), code=303)
        case "GET":
            return render_template('index.html')
        case _:
            return redirect(url_for('route_index'), code=404)

@app.route("/monitor", methods=["GET"])
def route_mon():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            while True:
                yield f'data: {stream.count:10d} - {stream.sum:0.03f}\n\n'
                time.sleep(5) # artificial delay. would rather push whenever values are updated. 
        return Response(events(), content_type='text/event-stream')
    return render_template('monitor.html')
    # return redirect(url_for('route_index'), code=404)

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

@app.route("/favicon", methods=["GET"])
def route_favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/png')


if __name__ == "__main__":
    # Data monitor should start as soon as the app is started.
    t = threading.Thread(target=stream.monitor)
    t.start()
    print('Starting webapp...')
    app.run(host='0.0.0.0', port=5000)