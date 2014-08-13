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
import logging.config
import os
import sys
from mongoengine import connect
from ConfigParser import SafeConfigParser
from gettext import gettext as _

if os.path.exists("/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg"):
    sys.path.insert(0, "/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg")
from flask import Flask, jsonify, render_template, url_for

# app instantiation needs to be before the cds.controllers import
# circular reference is in play here
app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

from pulp.cds.controllers import cds_api
from pulp.cds.controllers import cds_cluster_api

@app.route("/site-map")
def site_map():
    endpoints = []
    for rule in app.url_map.iter_rules():
        info = {}
        info["endpoint"] = str(rule)
        info["methods"] = str(rule.methods)
        info["arguments"] = str(rule.arguments)
        info["defaults"] = str(rule.defaults)
        endpoints.append(info)
    return jsonify(result={"endpoints": endpoints})



##
# Configuration
##
CONFIG = None # ConfigParser.SafeConfigParser instance
CONFIG_DEFAULT_FILE = "/etc/rhui/rhui_cds.conf"
CONFIG_DEFAULT_VALUES = {
    'database': {
        'name': 'rhui_cds',
        'host': 'localhost',
        'port': '27017',
    },
    'logs': {
        'config': '/etc/rhui/cds/logging.cfg',
    },
}

def check_config_file(config_file):
    if not os.access(config_file, os.F_OK):
        raise RuntimeError('Cannot find configuration file: %s' % config_file)
    if not os.access(config_file, os.R_OK):
        raise RuntimeError('Cannot read configuration file: %s' % config_file)
    return True


def load_configuration(config_file):
    global CONFIG
    check_config_file(config_file)
    CONFIG = SafeConfigParser()
    # add the defaults first
    for section, settings in CONFIG_DEFAULT_VALUES.items():
        CONFIG.add_section(section)
        for option, value in settings.items():
            CONFIG.set(section, option, value)
    # read the config files
    return CONFIG.read([config_file])


def configure_logging(log_config_file):
    if not os.access(log_config_file, os.R_OK):
        raise RuntimeError("Unable to read log configuration file: %s" % (log_config_file))
    logging.config.fileConfig(log_config_file)


##
# App Initialization
##
def initialize(config_file=None):
    global log

    if not config_file:
        config_file = CONFIG_DEFAULT_FILE
    load_configuration(config_file)
    
    db_name = CONFIG.get("database", "name")
    db_host = CONFIG.get("database", "host")
    db_port = CONFIG.getint("database", "port")
    log_config_file = CONFIG.get("logs", "config")

    configure_logging(log_config_file)
    log = logging.getLogger(__name__)
    db = connect(db_name, host=db_host, port=db_port)
    log.info("Connected to MongoDB at %s:%s using database name '%s'" % (db_host, db_port, db_name))
