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

from stripe.db import api as db_api
from stripe.tests.api.v1 import base
from stripe.tests.db import utils


class TestQueueMembersEmpty(base.FunctionalTest):

    def test_empty_get_all(self):
        res = self.get_json('/queues/1/members')
        self.assertEqual(res, [])

    def test_empty_get_one(self):
        res = self.get_json(
            '/queues/1/members/1', expect_errors=True
        )
        self.assertEqual(res.status_int, 500)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(res.json['error_message'])


class TestCase(base.FunctionalTest):

    def setUp(self):
        super(TestCase, self).setUp()
        self.db_api = db_api.get_instance()
        member = utils.get_test_member()
        self.db_api.create_member(member)
        queue = utils.get_test_queue()
        self.db_api.create_queue(queue)

    def _create_test_queue_member(self, **kwargs):
        queue_member = utils.get_test_queue_member(**kwargs)
        self.db_api.create_queue_member(queue_member)
        return queue_member

    def test_list_queue_members(self):
        queue_members = []
        qm = self._create_test_queue_member()
        queue_members.append(qm)
        res = self.get_json('/queues/%s/members' % qm['queue_id'])
        res.sort()
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        for idx in range(len(res)):
            self._assertEqualObjects(
                queue_members[idx], res[idx], ignored_keys
            )

    def test_delete_queue_member(self):
        qm = self._create_test_queue_member()
        self.delete(
            '/queues/%s/members/%s' % (qm['queue_id'], qm['id']), status=200
        )
        res = self.get_json('/queues/%s/members' % qm['queue_id'])
        res.sort()
        self.assertEqual(res, [])

    def test_get_queue_member(self):
        qm = self._create_test_queue_member()
        res = self.get_json(
            '/queues/%s/members/%s' % (qm['queue_id'], qm['id'])
        )
        ignored_keys = [
            'created_at',
            'updated_at',
        ]
        self._assertEqualObjects(qm, res, ignored_keys)

    def test_create_queue_member(self):
        json = {
            'member_id': 123,
        }
        res = self.post_json(
            '/queues/123/members', params=json, status=200
        )
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')

    def test_edit_queue_member(self):
        qm = self._create_test_queue_member()
        json = {
            'disabled': True,
        }
        res = self.get_json('/queues/%s/members' % qm['queue_id'])
        q = res[0]
        self.put_json(
            '/queues/%s/members/%s' % (q['queue_id'], q['id']), params=json
        )
        queue_member = self.db_api.get_queue_member(q['id'])
        self.assertEquals(queue_member.disabled, json['disabled'])
