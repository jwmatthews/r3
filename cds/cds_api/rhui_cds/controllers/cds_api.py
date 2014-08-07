#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the License
# (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied, including the
# implied warranties of MERCHANTABILITY, NON-INFRINGEMENT, or FITNESS FOR A
# PARTICULAR PURPOSE.
# You should have received a copy of GPLv2 along with this software;
# if not, see http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

import logging
from flask import jsonify, request

from rhui_cds import app
from rhui_cds.exceptions import *
from rhui_cds.managers.cds import CDSManager
from rhui_cds.models.cds import CDS

log = logging.getLogger(__name__)

# This wsgi app is registered at '/pulp/cds' 
# so this is the prefix to all URLs mentioned below in the route

cds_manager = CDSManager()

def log_request_params():
    log.info("request.data = <%s>" % (request.data))
    log.info("request.form = <%s>" % (request.form))
    log.info("request.args = <%s>" % (request.args))
    log.info("request.values = <%s>" % (request.values))
    log.info("request.headers = <%s>" % (request.headers))

@app.route("/", methods=["GET"])
def list_cdses():
    all_cdses = cds_manager.get_all()
    log.info("all_cdses = %s" % (all_cdses))
    return all_cdses.to_json()

@app.route("/", methods=["POST"])
def create_cds():
    log_request_params()
    data = request.get_json(force=True)
    log.info("Creating CDS with: %s" % (data))
    cds = cds_manager.create(**data)
    return cds.to_json()

@app.route("/<hostname>/", methods=["DELETE"])
def delete_cds(hostname):
    log.info("Delete CDS: '%s'" % (hostname))
    ret_val = cds_manager.delete(hostname)
    return ret_val.to_json()

@app.route("/<hostname>/", methods=["PUT"])
def update_cds(hostname):
    log.info("Update CDS: '%s'" % (hostname))
    log_request_params()
    data = request.get_json(force=True)
    if "hostname" in data.keys():
        del data["hostname"]
    cds = cds_manager.update(hostname=hostname, **data)
    return cds.to_json()

@app.route("/<hostname>/", methods=["GET"])
def info_cds(hostname):
    c = cds_manager.get(hostname)
    if not c:
        raise MissingResource("No CDS with hostname: '%s'" % hostname)
    return c.to_json()

@app.route("/<hostname>/history", methods=["GET"])
def cds_sync_histories(hostname):
    return "Stub: CDS Sync Histories for hostname '%s'" % (hostname)

@app.route("/<hostname>/sync", methods=["POST"])
def cds_sync(hostname):
    # Allow limiting what is sync by parameter data
    return "Stub: CDS Sync of hostname '%s'" % (hostname)
