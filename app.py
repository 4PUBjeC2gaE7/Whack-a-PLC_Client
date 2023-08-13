from __future__ import division
from flask import Flask, Response, render_template, request, redirect, send_from_directory, url_for, session, abort
from flask_session import Session
from pymodbus.client import ModbusTcpClient
from enum import Enum
from random import randrange, choice
from os import path
import itertools
import threading
import time
import json

# Constants
myServerAddr = '192.168.0.10'
clickSw = {
    'red':   10000,
    'yellow':10002,
    'green': 10001,
    'blue':  10003
}
clickLed = {
    'red':   0x2000,
    'yellow':0x2002,
    'green': 0x2001,
    'blue':  0x2003
}
scoreAddr = 0x0001

# Configure app
app = Flask(__name__)

# Connect to modbus server
client = ModbusTcpClient(myServerAddr)
client.connect()

# Generate streaming data and calculate statistics from it
class MyStreamMonitor(object):
    def __init__(self):
        self.state = {
            'red':False,
            'yellow':False,
            'green':False,
            'blue':False,
            'score':-1
        }
    
    def monitor(self, report_interval=1):
        print('Starting data stream...')
        if client.connected:
            Loopy = True
            while Loopy is True:
                time.sleep(.1)  # an artificial delay
                try:
                    # Read LED indicators
                    for select in clickLed:
                        self.state[select] = client.read_coils(clickLed[select]).bits[0]
                    self.state['score'] = client.read_holding_registers(scoreAddr).registers[0]
                except KeyboardInterrupt:
                    Loopy = False
            client.close()

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

@app.route("/data-stream", methods=["GET"])
def route_data():
    if request.headers.get('accept') == 'text/event-stream':
        def event_stream():
            laststate = stream.state.copy()
            while True:
            #    yield f'data: {json.dumps(stream.state)}\n\n'
                if laststate != stream.state:
                    laststate = stream.state.copy()
                    # yield f'{json.dumps(stream.state)}\n\n'
                    yield f'data: {json.dumps(stream.state)}\n\n'
                    # yield "here\n\nthere\n\n"
                time.sleep(0.1)
        return Response(event_stream(), content_type='text/event-stream')
    # fail-through
    return redirect(url_for('route_index'), code=404)

@app.route("/monitor", methods=["GET"])
def route_mon():
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