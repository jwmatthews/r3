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
from rhui_cds.managers.cds import CDSManager

log = logging.getLogger(__name__)

# This wsgi app is registered at '/pulp/cds' 
# so this is the prefix to all URLs mentioned below in the route

GET = "GET"
POST = "POST"
DELETE = "DELETE"
PUT = "PUT"

cds_manager = CDSManager()

@app.route("/", methods=[GET])
def list_cdses():
    all_cdses = cds_manager.get_all()
    log.info("all_cdses = %s" % (all_cdses))
    return jsonify(response=all_cdses)

@app.route("/<hostname>/", methods=[POST])
def create_cds(hostname):
    log.info("Creating CDS with hostname: %s" % (hostname))
    c = cds_manager.create(hostname)
    log.info("CDS created: %s" % (c))
    return jsonify(response=c)

@app.route("/<hostname>/", methods=[DELETE])
def delete_cds(hostname):
    log.info("Delete CDS: '%s'" % (hostname))
    cds_manager.delete(hostname)

@app.route("/<hostname>/", methods=[PUT])
def update_cds(hostname):
    return "Stub: CDS Update of hostname '%s'" % (hostname)

@app.route("/<hostname>/", methods=[GET])
def info_cds(hostname):
    c = cds_manager.get(hostname)
    return jsonify(c)

@app.route("/<hostname>/history", methods=[GET])
def cds_sync_histories(hostname):
    return "Stub: CDS Sync Histories for hostname '%s'" % (hostname)

@app.route("/<hostname>/sync", methods=[POST])
def cds_sync(hostname):
    # Allow limiting what is sync by parameter data
    return "Stub: CDS Sync of hostname '%s'" % (hostname)
