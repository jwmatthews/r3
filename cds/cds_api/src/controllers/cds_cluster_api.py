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

from rhui_cds import app

# This wsgi app is registered at '/pulp/cds' 
# so this is the prefix to all URLs mentioned below in the route

@app.route("/cluster", methods=["GET"])
def list_clusters():
    return "Stub: List All CDS Clusters"

@app.route("/cluster/<cluster_id>/", methods=["POST"])
def create_cluster(cluster_id):
    return "Stub: CDS Cluster Created with cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/", methods=["DELETE"])
def delete_cluster(cluster_id):
    return "Stub: CDS Cluster Delete of cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/", methods=["PUT"])
def update_cluster(cluster_id):
    return "Stub: CDS Cluster Update of cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/", methods=["GET"])
def info_cluster(cluster_id):
    return "Stub: CDS Cluster Info of cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/history", methods=["GET"])
def cluster_sync_histories(cluster_id):
    return "Stub: CDS Cluster Sync Histories for cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/sync", methods=["POST"])
def cluster_sync(cluster_id):
    # Allow limiting what is sync by parameter data
    return "Stub: CDS Cluster Sync of cluster_id '%s'" % (cluster_id)
