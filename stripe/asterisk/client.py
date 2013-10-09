# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

from sarlacc.asterisk import client

from stripe.asterisk import models
from stripe.openstack.common import log as logging


class Client(object):

    log = logging.getLogger('asterisk.Client')

    def __init__(self, app):
        super(Client, self).__init__()
        self.app = app
        self.agi = client.AGI()
        self.handle_answer()

    def handle_answer(self):
        self.log.debug('Handle answer')
        self.agi.answer()
        self.agi.set_music(True)
        event = models.ClientEvent(queue='1')
        event.type = 'answer'
        event.data = self._build_queue_caller()
        self.app.add_event(event)

    def handle_position(self, position):
        self.agi.set_music(False)
        if position > 0:
            self.agi.stream_file('queue-thereare')
            self.agi.say_number(position)
            self.agi.stream_file('queue-callswaiting')
        else:
            self.agi.stream_file('queue-youarenext')
        self.agi.set_music(True)

    def _build_queue_caller(self):
        data = {
            'called_id': self._get_called_id(),
            'caller_id': self._get_caller_id(),
            'caller_name': self._get_caller_name(),
        }

        return data

    def _get_called_id(self):
        try:
            res = self.agi.env['agi_extension']
        except Exception:
            res = 's'

        return res

    def _get_caller_id(self):
        try:
            res = self.agi.env['agi_callerid']
        except Exception:
            res = 'unknown'

        return res

    def _get_caller_name(self):
        try:
            res = self.agi.env['agi_calleridname']
        except Exception:
            res = 'unknown'

        return res