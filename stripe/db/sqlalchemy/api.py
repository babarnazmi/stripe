# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
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

"""SQLAlchemy storage backend."""

from sqlalchemy.orm.exc import NoResultFound

from stripe.common import exception
from stripe.db import api
from stripe.db.sqlalchemy import models
from stripe.openstack.common.db.sqlalchemy import session as db_session
from stripe.openstack.common import log as logging

LOG = logging.getLogger(__name__)

get_session = db_session.get_session


def get_backend():
    """The backend is this module itself."""
    return Connection()


def model_query(model, *args, **kwargs):
    """Query helper for simpler session usage.

    :param session: if present, the session to use
    """

    session = kwargs.get('session') or get_session()
    query = session.query(model, *args)
    return query


class Connection(api.Connection):
    """SqlAlchemy connection."""

    def __init__(self):
        pass

    def create_queue(self, values):
        queue = models.Queue()
        queue.update(values)
        queue.save()
        return queue

    def get_queue(self, queue):
        query = model_query(models.Queue).filter_by(id=queue)
        try:
            result = query.one()
        except NoResultFound:
            raise exception.QueueNotFound(queue=queue)

        return result

    def get_queue_list(self):
        query = model_query(models.Queue.id)
        return [i[0] for i in query.all()]