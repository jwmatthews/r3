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

config = None # ConfigParser.SafeConfigParser instance
_config_files = ['/etc/rhui/rhui_cds.conf',]

from rhui_cds.controllers import cds_api
from rhui_cds.controllers import cds_cluster_api

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
_default_values = {
    'database': {
        'name': 'rhui_cds',
        'seeds': 'localhost:27017',
    },
    'logs': {
        'config': '/etc/rhui/cds/logging.cfg',
    },
}

def check_config_files():
    """
    Check for read permissions on the configuration files. Raise a runtime error
    if the file doesn't exist or the read permissions are lacking.
    """
    for f in _config_files:
        if not os.access(f, os.F_OK):
            raise RuntimeError('Cannot find configuration file: %s' % f)
        if not os.access(f, os.R_OK):
            raise RuntimeError('Cannot read configuration file: %s' % f)
    return True


def load_configuration():
    """
    Check the configuration files and load the global 'config' object from them.
    """
    global config
    check_config_files()
    config = SafeConfigParser()
    # add the defaults first
    for section, settings in _default_values.items():
        config.add_section(section)
        for option, value in settings.items():
            config.set(section, option, value)
    # read the config files
    return config.read(_config_files)

##
# Logging
##
TIME = '%(asctime)s'
LEVEL = ' [%(levelname)s]'
THREAD = '[%(threadName)s]'
FUNCTION = ' %(funcName)s()'
FILE = ' @ %(filename)s'
LINE = ':%(lineno)d'
MSG = ' - %(message)s'

if sys.version_info < (2,5):
    FUNCTION = ''

FMT = \
    ''.join((TIME,
            LEVEL,
            THREAD,
            FUNCTION,
            FILE,
            LINE,
            MSG,))


def check_log_file(file_path):
    """
    Check the write permissions on log files and their parent directory. Raise
    a runtime error if the write permissions are lacking.
    """
    if os.path.exists(file_path) and not os.access(file_path, os.W_OK):
        raise RuntimeError('Cannot write to log file: %s' % file_path)
    dir_path = os.path.dirname(file_path)
    if not os.access(dir_path, os.W_OK):
        raise RuntimeError('Cannot write to log directory: %s' % dir_path)
    return 'Yeah!'

def configure_logging():
    """
    Configures logging from config file specified in rhui_cds.conf
    """
    log_config_filename = config.get('logs', 'config')
    if not os.access(log_config_filename, os.R_OK):
        raise RuntimeError("Unable to read log configuration file: %s" % (log_config_filename))
    logging.config.fileConfig(log_config_filename)


##
# App Initialization
##
def initialize(db_name=None):
    load_configuration()
    configure_logging()
    if not db_name:
        db_name = config.get("database", "name")
    db = connect(db_name)
