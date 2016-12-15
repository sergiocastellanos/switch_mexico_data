# -*- coding: utf-8 -*-

import pandas as pd
from shapely.geometry import Point, shape

from flask import Flask
from flask import render_template
import json

from flask.json import jsonify


data_path = './input/'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/nodes")
def get_nodes():
    with open(data_path + '/geojson/nodes/node1.json') as node1:
        node1 = json.load(node1)
    return jsonify(node1)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8080, threaded=True ,debug=True)
