import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../../src")

if sys.version_info < (2,7):
    # python 2.6
    import unittest2 as unittest
else:
    # python 2.7 and greater
    import unittest

from pulp_cds.cds import initialize
from pulp_cds.cds.models.cds import CDS
from pulp_cds.cds.models.cds_cluster import Cluster

import pulp_cds.cds
config_file_for_unittests = os.path.join(os.path.abspath(os.path.dirname(__file__)), "./config/unittests.conf")
pulp_cds.cds._config_files = [config_file_for_unittests]

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config/unittests.cfg")

class BaseTestCase(unittest.TestCase):
    def drop_collections(self):
        # Remember to drop the collections instead of the entire DB
        # Dropping the entire DB can mess up indexes
        # Removing the unique index leading to odd behavior in unit tests
        CDS.drop_collection()
        Cluster.drop_collection()

    def setUp(self):
        pulp_cds.cds.app.config['TESTING'] = True
        pulp_cds.cds.initialize(CONFIG_FILE)
        self.app = pulp_cds.cds.app.test_client()
        self.drop_collections()

    def tearDown(self):
        pass
