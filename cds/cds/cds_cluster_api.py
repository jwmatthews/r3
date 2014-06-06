from flask import request

from cds import app
from cds.cds_api import GET, POST, DELETE, PUT

# This wsgi app is registered at '/pulp/cds' 
# so this is the prefix to all URLs mentioned below in the route

@app.route("/cluster", methods=[GET])
def list_clusters():
    return "Stub: List All CDS Clusters"

@app.route("/cluster/<cluster_id>/", methods=[POST])
def create_cluster(cluster_id):
    return "Stub: CDS Cluster Created with cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/", methods=[DELETE])
def delete_cluster(cluster_id):
    return "Stub: CDS Cluster Delete of cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/", methods=[PUT])
def update_cluster(cluster_id):
    return "Stub: CDS Cluster Update of cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/", methods=[GET])
def info_cluster(cluster_id):
    return "Stub: CDS Cluster Info of cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/history", methods=[GET])
def cluster_sync_histories(cluster_id):
    return "Stub: CDS Cluster Sync Histories for cluster_id '%s'" % (cluster_id)

@app.route("/cluster/<cluster_id>/sync", methods=[POST])
def cluster_sync(cluster_id):
    # Allow limiting what is sync by parameter data
    return "Stub: CDS Cluster Sync of cluster_id '%s'" % (cluster_id)
