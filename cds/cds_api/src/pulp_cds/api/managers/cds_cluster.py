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
from mongoengine.fields import *
from pulp_cds.cds.exceptions import *
from pulp_cds.cds.models.cds_cluster import Cluster

log = logging.getLogger(__name__)

class CDSClusterManager():

    def create(self, **params):
        """
        params - dictionary
        """
        c = Cluster(**params)
        c.save(force_insert=True)
        return c

    def get_all(self):
        return Cluster.objects()

    def get(self, cluster_id):
        c = Cluster.objects(cluster_id=cluster_id)
        if len(c) < 1:
            return None
        return c[0]

    def update(self, cluster_id, **params):
        c = self.get(cluster_id)
        if not c:
            raise MissingResource("No Cluster with cluster_id: '%s'" % cluster_id)
        for k in params.keys():
            c[k] = params[k]
        c.save()
        cluster = Cluster.objects(cluster_id=cluster_id)
        return cluster[0]
