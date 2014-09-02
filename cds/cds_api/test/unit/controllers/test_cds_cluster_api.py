import json
import logging
import os
import pytz
import sys
from bson import json_util
from datetime import datetime

from mongoengine.errors import NotUniqueError

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")
import base

from pulp_cds.cds.models.cds import CDS
from pulp_cds.cds.models.cds_cluster import Cluster

log = logging.getLogger(__name__)


class TestCDSCluster_API(base.BaseTestCase):
    def setUp(self):
        super(TestCDSCluster_API, self).setUp()

    def tearDown(self):
        super(TestCDSCluster_API, self).tearDown()

    def test_list_clusters(self):
        resp = self.app.get('/cluster/')
        items = json.loads(resp.data)
        self.assertEquals(len(items), 0)

        cluster_id_1 = "unit_test_cluster_1"
        cluster_id_2 = "unit_test_cluster_2"

        cluster1 = Cluster(cluster_id=cluster_id_1)
        cluster2 = Cluster(cluster_id=cluster_id_2)

        cluster1.save(force_insert=True)
        cluster2.save(force_insert=True)

        resp = self.app.get('/cluster/')
        self.assertEquals(resp.status_code, 200)
        clusters = json.loads(resp.data)
        self.assertEquals(len(clusters), 2)
        for c in clusters:
            self.assertIn(c["cluster_id"], [cluster_id_1, cluster_id_2])

    def test_create(self):
        cluster_id = "unit_test_cluster"

        data = {"cluster_id": cluster_id}
        json_data = json.dumps(data)

        resp = self.app.post('/cluster/', data=json_data, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        cluster = json.loads(resp.data)
        self.assertEquals(cluster["cluster_id"], cluster_id)

    def test_create_already_exists(self):
        cluster_id = "unit_test_cluster"

        cluster1 = Cluster(cluster_id=cluster_id)
        cluster1.save(force_insert=True)

        data = {"cluster_id": cluster_id}
        json_data = json.dumps(data)

        resp = self.app.post('/cluster/', data=json_data, content_type='application/json')
        self.assertEquals(resp.status_code, 409)

    def test_info_cluster(self):
        cluster_id = "unit_test_cluster"
        cluster1 = Cluster(cluster_id=cluster_id)
        cluster1.save(force_insert=True)

        resp = self.app.get("/cluster/%s/" % (cluster_id))
        self.assertEquals(resp.status_code, 200)
        cluster = json.loads(resp.data)
        self.assertEquals(cluster["cluster_id"], cluster_id)

    def test_update(self):
        cluster_id = "unit_test_cluster"
        cluster1 = Cluster(cluster_id=cluster_id, cdses=[])
        cluster1.save(force_insert=True)
        cluster1.reload()

        self.assertEquals(len(cluster1["cdses"]), 0)

        cds1 = CDS(hostname='unit_test_cds_1', cluster_id='unit_test_cluster')
        cds1.save(force_insert=True)

        data = {"cluster_id": cluster_id, "cdses": ['unit_test_cds_1']}
        json_data = json.dumps(data)

        resp = self.app.put("/cluster/%s/" % (cluster_id), data=json_data, content_type='application/json')
        self.assertEquals(resp.status_code, 200)

        # Using json_util.loads so it can parse the {"$date":value} formats for created_at/updated_at
        cluster_updated = json_util.loads(resp.data)
        self.assertNotEquals(len(cluster_updated["cdses"]), 0)
