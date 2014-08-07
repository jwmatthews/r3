from datetime import datetime

from mongoengine import *
from mongoengine import signals

from rhui_cds.models.cds import CDS
from rhui_cds.models.cds_cluster import Cluster 

def update_timestamp(sender, document, **kwargs):
    document.updated_at = datetime.utcnow()

signals.pre_save.connect(update_timestamp, sender=CDS)
signals.pre_save.connect(update_timestamp, sender=Cluster)
