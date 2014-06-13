import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")

try:
    # python 2.6
    import unittest2 as unittest
except:
    # python 2.7 and greater
    import unittest


from mongoengine import connect
from mongoengine.connection import _get_db

from rhui_cds import initialize
import rhui_cds
config_file_for_unittests = os.path.join(os.path.abspath(os.path.dirname(__file__)), "./config/unittests.conf")
rhui_cds._config_files = [config_file_for_unittests]

DB_NAME = "test_rhui_cds"

class BaseTestCase(unittest.TestCase):
    def drop_test_database(self):
        db = _get_db()
        db.connection.drop_database(DB_NAME)

    def setUp(self):
        initialize(DB_NAME) 
        self.drop_test_database()

    def tearDown(self):
        pass