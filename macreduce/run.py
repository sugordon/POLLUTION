#!/usr/bin/env python
"""Instantiates the Python Eve REST API Server.

Instantiates the Python Eve REST API Server for both local
and cloud (IBM Bluemix) execution.  Provides a default catch-all
routing to provide API consumers with intentional responses
for all routes.  Provides a redis cloud caching instance for
session management where desired.
"""

from settings import (REDIS_INSTANCE,
                      APP_HOST,
                      APP_PORT,
                      VCAP_CONFIG)
from flask.ext.bootstrap import Bootstrap
from eve import Eve
from eve_docs import eve_docs
from routes import home
from gevent import wsgi, monkey, socket
import os

__author__ = "Sanjay Joshi"
__copyright__ = "IBM Copyright 2015"
__credits__ = ["Sanjay Joshi"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Sanjay Joshi"
__email__ = "joshisa@us.ibm.com"
__status__ = "Prototype"

# Monkey Patching app behavior to make it greenlet non-blocking
# This is usually required by gevent for native bindings for things
# like Redis interactions, etc ...
monkey.patch_all()
socket.setdefaulttimeout(240)
# capture current working directory
PWD = os.environ.get("PWD")
# set static folder path for static data
static_folder = os.path.join(PWD, "macreduce/static")

# Detect if we are deployed within Bluemix or not and configure accordingly
if VCAP_CONFIG:
    print 'Welcome to Bluemix'
    print 'Running on Python Version: 2.7.9'

    app = Eve(static_folder=static_folder,
              redis=REDIS_INSTANCE)
    REDIS_INSTANCE.flushdb()

else:
    print 'We are not running in Bluemix! Dev Mode Enabled'
    app = Eve(static_folder=static_folder,
              redis=REDIS_INSTANCE)
    print '  Enabling Debug ...'
    app.debug = True

# Setup some default home page path rules for JSON and HTML
app.add_url_rule('/', 'index', home.index)
# app.add_url_rule('/<path:path>', 'nonresource', home.index)
# Setup a favicon url for the home page
app.add_url_rule('/favicon', 'favicon',
                 view_func=home.favicon, methods=['GET'])
app.add_url_rule('/populate', 'populate',
                 view_func=home.populate, methods=['GET'])

# Bootstrap and start Flask app within the WSGI GEvent Process
if __name__ == '__main__':
    # Required to enable the Eve-docs extension
    Bootstrap(app)
    # Let's cleanup our webhooks
    # poynthook.getWebhooks()

    # Register the Flask Eve-docs blueprint
    app.register_blueprint(eve_docs, url_prefix='/docs')
    # Example invocation for running the Flask Server by itself
    # app.run(host=APP_HOST, port=int(APP_PORT))

    # Starting the GEvent WSGI Server to host the Flask App
    # GEvent should provide superior response times to the
    # dev Flask server
    ws = wsgi.WSGIServer((APP_HOST, int(APP_PORT)), app)
    ws.serve_forever()
