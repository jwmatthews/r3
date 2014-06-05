# -*- coding: utf-8 -*-
#
# Copyright © 2014 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.

# python-flask-0.9-7.el6.noarch for RHEL-6 brings in python-jinja2-26-2.6-2.el6.noarch as a dep
# python-jinja2-26 is packaged differently as to not conflict with an older python-jinja based on 2.2
# We need to perform a workaround
import os
import sys
if os.path.exists("/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg"):
    sys.path.insert(0, "/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg")

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()