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


from flask import request

from pulp_cds.cds import app
from pulp_cds.cds.exceptions import *
from pulp_cds.cds.managers.cds import CDSManager
from pulp_cds.cds.managers.cds_cluster import CDSClusterManager
from pulp_cds.cds.models.cds_cluster import Cluster

log = logging.getLogger(__name__)

# This wsgi app is registered at '/pulp/cds/cluster' 
# so this is the prefix to all URLs mentioned below in the route

cds_manager = CDSManager()
cluster_manager = CDSClusterManager()

def log_request_params():
    log.info("request.data = <%s>" % (request.data))
    log.info("request.form = <%s>" % (request.form))
    log.info("request.args = <%s>" % (request.args))
    log.info("request.values = <%s>" % (request.values))
    log.info("request.headers = <%s>" % (request.headers))

@app.route("/cluster/", methods=["GET"])
def list_clusters():
    all_clusters = cluster_manager.get_all()
    log.info("all_clusters = %s" % (all_clusters))
    return all_clusters.to_json()

@app.route("/cluster/", methods=["POST"])
def create_cluster():
    log_request_params()
    data = request.get_json(force=True)
    log.info("Creating Cluster with: %s" % (data))
    cluster = cluster_manager.create(**data)
    return cluster.to_json()

@app.route("/cluster/<cluster_id>/", methods=["DELETE"])
def delete_cluster(cluster_id):
    return "Stub: CDS Cluster Delete of cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/", methods=["PUT"])
def update_cluster(cluster_id):
    log.info("Update Cluster: '%s'" % (cluster_id))
    log_request_params()
    data = request.get_json(force=True)
    if "cluster_id" in data.keys():
        del data["cluster_id"]
    if "cdses" in data.keys():
        cds_list = []
        for h in data['cdses']:
            cds = cds_manager.get(hostname=h) 
            cds_list.append(cds)
        data['cdses'] = cds_list
    cluster = cluster_manager.update(cluster_id=cluster_id, **data)
    return cluster.to_json()

@app.route("/cluster/<cluster_id>/", methods=["GET"])
def info_cluster(cluster_id):
    c = cluster_manager.get(cluster_id)
    if not c:
        raise MissingResource("No CDS Cluster with cluster_id: '%s'" % cluster_id)
    return c.to_json()

@app.route("/cluster/<cluster_id>/history", methods=["GET"])
def cluster_sync_histories(cluster_id):
    return "Stub: CDS Cluster Sync Histories for cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/sync", methods=["POST"])
def cluster_sync(cluster_id):
    # Allow limiting what is sync by parameter data
    return "Stub: CDS Cluster Sync of cluster_id '%s'" % (cluster_id)
