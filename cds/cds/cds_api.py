from flask import request

from cds import app

# This wsgi app is registered at '/pulp/cds' 
# so this is the prefix to all URLs mentioned below in the route

GET = "GET"
POST = "POST"
DELETE = "DELETE"
PUT = "PUT"

@app.route("/", methods=[GET])
def list_cdses():
    return "Stub: List All CDSes"

@app.route("/<hostname>/", methods=[POST])
def create_cds(hostname):
    return "Stub: CDS Created with hostname '%s'" % (hostname)

@app.route("/<hostname>/", methods=[DELETE])
def delete_cds(hostname):
    return "Stub: CDS Delete of hostname '%s'" % (hostname)

@app.route("/<hostname>/", methods=[PUT])
def update_cds(hostname):
    return "Stub: CDS Update of hostname '%s'" % (hostname)

@app.route("/<hostname>/", methods=[GET])
def info_cds(hostname):
    return "Stub: CDS Info of hostname '%s'" % (hostname)

@app.route("/<hostname>/history", methods=[GET])
def cds_sync_histories(hostname):
    return "Stub: CDS Sync Histories for hostname '%s'" % (hostname)

@app.route("/<hostname>/sync", methods=[POST])
def cds_sync(hostname):
    # Allow limiting what is sync by parameter data
    return "Stub: CDS Sync of hostname '%s'" % (hostname)
