import logging
import os
import sys

from mongoengine.errors import NotUniqueError

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")
import base

from pulp_cds.api.managers.cds import CDSManager

log = logging.getLogger(__name__)


class TestCDSManager(base.BaseTestCase):
    def setUp(self):
        super(TestCDSManager, self).setUp()
        self.cds_manager = CDSManager()

    def tearDown(self):
        super(TestCDSManager, self).tearDown()

    def test_simple_get_all(self):
        found = self.cds_manager.get_all()
        self.assertEquals(len(found), 0)

        hostnames = ["cds1.example.com", "cds2.example.com"]
        cluster_id = "unit_test_cluster"
        for h in hostnames:
            self.cds_manager.create(hostname=h, cluster_id=cluster_id)

        found = self.cds_manager.get_all()
        self.assertEquals(len(found), 2)

        for f in found:
            self.assertIn(f.hostname, hostnames)

    def test_simple_create(self):
        hostname = "cds1.example.com"
        cluster_id = "unit_test_cluster"
        c = self.cds_manager.create(hostname=hostname, cluster_id=cluster_id)
        self.assertIsNotNone(c)

        from pulp_cds.api.models.cds import CDS
        found = CDS.objects(hostname=hostname)
        self.assertEquals(found[0], c)

    def test_create_cds_already_exists(self):
        hostname = "cds1.example.com"
        cluster_id = "unit_test_cluster"
        c = self.cds_manager.create(hostname=hostname, cluster_id=cluster_id)
        self.assertIsNotNone(c)

        self.assertRaises(NotUniqueError,
                lambda: self.cds_manager.create(hostname=hostname, cluster_id=cluster_id))

    def test_delete(self):
        hostname = "cds1.example.com"
        cluster_id = "unit_test_cluster"
        c = self.cds_manager.create(hostname=hostname, cluster_id=cluster_id)

        from pulp_cds.api.models.cds import CDS
        found = CDS.objects(hostname=hostname)
        self.assertEquals(found[0], c)

        self.cds_manager.delete(hostname)
        found = CDS.objects(hostname=hostname)
        self.assertEquals(len(found), 0)

    def test_get(self):
        hostname = "cds1.example.com"
        cluster_id = "unit_test_cluster"
        found = self.cds_manager.get(hostname=hostname)
        self.assertIsNone(found)

        created = self.cds_manager.create(hostname=hostname, cluster_id=cluster_id)
        found = self.cds_manager.get(hostname=hostname)
        self.assertEquals(created, found)

    def test_update(self):
        pass


    def test_sync_history(self):
        pass

    def test_sync(self):
        pass
 
