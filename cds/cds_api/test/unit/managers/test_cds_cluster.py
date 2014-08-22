import logging
import os
import sys

from mongoengine.errors import NotUniqueError

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")
import base

from pulp_cds.cds.managers.cds_cluster import CDSClusterManager

log = logging.getLogger(__name__)


class TestCDSClusterManager(base.BaseTestCase):
    def setUp(self):
        super(TestCDSClusterManager, self).setUp()
        self.cds_cluster_manager = CDSClusterManager()

    def tearDown(self):
        super(TestCDSClusterManager, self).tearDown()

    def test_simple_get_all(self):
        found = self.cds_cluster_manager.get_all()
        self.assertEquals(len(found), 0)

        cluster_ids = ["cds_cluster1", "cds_cluster2"]
        for cid in cluster_ids:
            self.cds_cluster_manager.create(cluster_id=cid)

        found = self.cds_cluster_manager.get_all()
        self.assertEquals(len(found), 2)

        for f in found:
            self.assertIn(f.cluster_id, cluster_ids)

    def test_simple_create(self):
        cid = "cds_cluster1"
        c = self.cds_cluster_manager.create(cluster_id=cid)
        self.assertIsNotNone(c)

        from pulp_cds.cds.models.cds_cluster import Cluster
        found = Cluster.objects(cluster_id=cid)
        self.assertEquals(found[0], c)

    def test_create_cds_already_exists(self):
        cid = "cds_cluster1"
        c = self.cds_cluster_manager.create(cluster_id=cid)
        self.assertIsNotNone(c)

        self.assertRaises(NotUniqueError,
                lambda: self.cds_cluster_manager.create(cluster_id=cid))

    def test_delete(self):
        pass

    def test_get(self):
        pass

    def test_update(self):
        pass


    def test_sync_history(self):
        pass

    def test_sync(self):
        pass
 
