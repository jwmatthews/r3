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

from datetime import datetime

from mongoengine import *

from pulp_cds.cds.models.cds import CDS

class Cluster(Document):
    #cluster_id = StringField(required=True, unique=True, primary_key=True)
    cluster_id = StringField(required=True, unique=True)
    cdses = ListField(StringField())
    #cdses = ListField(ReferenceField(CDS))
    created_at = DateTimeField(required=True, default=datetime.utcnow())
    sync_schedule = StringField(required=False)
    repos = ListField(StringField())
    meta = {'collection': 'cluster'}

