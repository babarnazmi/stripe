# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
# Copyright (C) 2013 PolyBeacon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Stripe Service API
"""

import logging

from oslo.config import cfg
from wsgiref import simple_server

from stripe.api import app
from stripe.common import config
from stripe.openstack.common import log

CONF = cfg.CONF

LOG = log.getLogger(__name__)


def main():
    config.parse_args()
    log.setup('stripe')
    host = CONF.bind_host
    port = CONF.bind_port
    wsgi = simple_server.make_server(
        host, port, app.VersionSelectorApplication()
    )

    LOG.info('Serving on http://%s:%s' % (host, port))
    LOG.info('Configuration:')
    CONF.log_opt_values(LOG, logging.INFO)

    try:
        wsgi.serve_forever()
    except KeyboardInterrupt:
        pass
