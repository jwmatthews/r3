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

from pulp.cds.models.cds import CDS

log = logging.getLogger(__name__)


class TestCDS_API(base.BaseTestCase):
    def setUp(self):
        super(TestCDS_API, self).setUp()

    def tearDown(self):
        super(TestCDS_API, self).tearDown()

    def test_list_cdses(self):
        resp = self.app.get('/')
        items = json.loads(resp.data)
        self.assertEquals(len(items), 0)

        hostname1 = "cds1.example.com"
        hostname2 = "cds2.example.com"

        cds1 = CDS(hostname=hostname1)
        cds2 = CDS(hostname=hostname2)

        cds1.save(force_insert=True)
        cds2.save(force_insert=True)

        resp = self.app.get('/')
        self.assertEquals(resp.status_code, 200)
        cdses = json.loads(resp.data)
        self.assertEquals(len(cdses), 2)
        for c in cdses:
            self.assertIn(c["hostname"], [hostname1, hostname2])

    def test_create(self):
        hostname = "cds1.example.com"

        data = {"hostname":hostname}
        json_data = json.dumps(data)

        resp = self.app.post('/', data=json_data, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        cds = json.loads(resp.data)
        self.assertEquals(cds["hostname"], hostname)

    def test_create_already_exists(self):
        hostname = "cds1.example.com"
        cds1 = CDS(hostname=hostname)
        cds1.save(force_insert=True)

        data = {"hostname":hostname}
        json_data = json.dumps(data)

        resp = self.app.post('/', data=json_data, content_type='application/json')
        self.assertEquals(resp.status_code, 409)

    def test_info_cds(self):
        hostname = "cds1.example.com"
        cds1 = CDS(hostname=hostname)
        cds1.save(force_insert=True)

        resp = self.app.get("/%s/" % (hostname))
        self.assertEquals(resp.status_code, 200)
        cds = json.loads(resp.data)
        self.assertEquals(cds["hostname"], hostname)

    def test_update(self):
        hostname = "cds1.example.com"
        cds1 = CDS(hostname=hostname)
        cds1.save(force_insert=True)
        cds1.reload()

        data = {"hostname":hostname}
        json_data = json.dumps(data)

        resp = self.app.put("/%s/" % (hostname), data=json_data, content_type='application/json')
        self.assertEquals(resp.status_code, 200)

        # Using json_util.loads so it can parse the {"$date":value} formats for created_at/updated_at
        cds_updated = json_util.loads(resp.data)
        self.assertEquals(cds_updated["hostname"], cds1["hostname"])

        orig_created_at = pytz.utc.localize(cds1["created_at"])
        modified_created_at = cds_updated["created_at"]
        self.assertEquals(orig_created_at, modified_created_at)

        orig_updated_at = pytz.utc.localize(cds1["updated_at"])
        modified_updated_at = cds_updated["updated_at"]
        self.assertGreater(modified_updated_at, orig_updated_at)

    def test_delete(self):
        hostname = "cds1.example.com"
        cds1 = CDS(hostname=hostname)
        cds1.save(force_insert=True)

        resp = self.app.delete("/%s/" % (hostname))
        self.assertEquals(resp.status_code, 200)

        resp = self.app.get("/%s/" % (hostname))
        self.assertEquals(resp.status_code, 404)
