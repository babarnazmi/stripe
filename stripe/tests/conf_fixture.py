# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Author: Paul Belanger <paul.belanger@polybeacon.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.

import fixtures

from oslo.config import cfg

from stripe.common import config

CONF = cfg.CONF


class ConfFixture(fixtures.Fixture):
    """Fixture to manage global conf settings."""

    def __init__(self, conf):
        self.conf = conf

    def setUp(self):
        super(ConfFixture, self).setUp()

        self.conf.set_default('connection', "sqlite://", group='database')
        self.conf.set_default('sqlite_synchronous', False)
        self.conf.set_default('verbose', True)
        config.parse_args([], default_config_files=[])
        self.addCleanup(self.conf.reset)