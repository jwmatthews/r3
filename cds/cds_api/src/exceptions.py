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
# You should have received a copy of GPLv2 along with this software; if not,
# see http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

import logging
from flask import jsonify
from mongoengine.errors import OperationError, NotUniqueError

from pulp.cds import app

log = logging.getLogger(__name__)

class ApiException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv    

class InvalidUsage(ApiException):
    status_code = 400

class MissingResource(ApiException):
    status_code = 404


###
# Order is important for registering the error handlers
# Order as:  Most Specific exception class to least specific
###
@app.errorhandler(ApiException)
def handle_api_exception(error):
    log.exception(error)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(NotUniqueError)
def handle_mongoengine_not_unique_error(error):
    log.exception(error)
    status_code = 409
    info = {"message": str(error), "status_code": status_code}
    response = jsonify(info)
    response.status_code = status_code
    return response

@app.errorhandler(OperationError)
def handle_mongoengine_operation_error(error):
    log.exception(error)
    status_code = 400
    info = {"message": str(error), "status_code": status_code}
    response = jsonify(info)
    response.status_code = status_code
    return response

@app.errorhandler(BaseException)
def handle_base_exception(error):
    log.exception(error)
    status_code = 500
    info = {"message": str(error), "status_code": status_code}
    response = jsonify(info)
    response.status_code = status_code
    return response

@app.errorhandler(AssertionError)
def handle_assertion_error(error):
    log.exception(error)
    status_code = 400
    info = {"message": str(error), "status_code": status_code}
    response = jsonify(info)
    response.status_code = status_code
    return response
