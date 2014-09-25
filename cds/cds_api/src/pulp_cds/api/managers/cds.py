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

from pulp_cds.cds.exceptions import *
from pulp_cds.cds.models.cds import CDS

log = logging.getLogger(__name__)

class CDSManager():

    def create(self, **params):
        """
        params - dictionary
        """
        c = CDS(**params)
        c.save(force_insert=True)
        return c

    def delete(self, hostname):
        c = self.get(hostname)
        if not c:
            raise MissingResource("No CDS with hostname: '%s'" % hostname)
        c.delete()
        return c

    def update(self, hostname, **params):
        c = self.get(hostname)
        if not c:
            raise MissingResource("No CDS with hostname: '%s'" % hostname)
        for k in params.keys():
            c[k] = params[k]
        c.save()
        cdses = CDS.objects(hostname=hostname)
        return cdses[0]

    def get(self, hostname):
        c = CDS.objects(hostname=hostname)
        if len(c) < 1:
            return None
        return c[0]

    def get_all(self):
        return CDS.objects()

    def sync_history(self):
        pass

    def sync(self, repos=None):
        pass
