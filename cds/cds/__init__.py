import os
import sys
if os.path.exists("/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg"):
    sys.path.insert(0, "/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg")

from flask import Flask, jsonify, render_template, url_for
app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

from cds import cds_api
from cds import cds_cluster_api

@app.route("/hello", methods=["GET"])
def hello():
    return "Hello world"

@app.route("/site-map")
def site_map():
    endpoints = []
    for rule in app.url_map.iter_rules():
        info = {}
        info["endpoint"] = str(rule)
        info["methods"] = str(rule.methods)
        info["arguments"] = str(rule.arguments)
        info["defaults"] = str(rule.defaults)
        endpoints.append(info)
    return jsonify(result={"endpoints": endpoints})

