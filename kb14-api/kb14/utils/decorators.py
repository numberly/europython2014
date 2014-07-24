#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import gevent
import json
import uwsgi

from functools import update_wrapper
from pymongo.errors import AutoReconnect
from uwsgidecorators import spooler_functions


def job(f):
    """A decorator that gives asynchronicity and database fault-tolerance for
    the decorated function.

    The decorated function is added to *uwsgidecorators.spooler_function*, so it
    can be spooled like any other spoolraw function with uwsgi.spool.

    Three methods are added to the function:
    * function.perform(): simply execute the decorated function (can be usefull
    if we want a particular function to be asynchronous only in some contexts);
    * function.spawn(): execute the function in a gevent greenlet;
    * function.spool(): ask a uWSGI mule to spool this function (see
    :mod:`kb14.utils.mule` for why we are using a mule).

    Also, the *function.__call__* method is slightly modified to handle the two
    possibles contexts (spawned, spooled): if the function is exectued by the
    spooler, we want to init the database, because the spooler doesn't have the
    application context.
    Otherwise, we just try to execute the function and spool it if there is a
    database problem (i.e. a :class:`pymongo.errors.AutoReconnect` is raised).

    The decorated function should always be called with *function.spawn()*, so
    that it first tries to execute it in a greenlet, and spool it if a problem
    occurs.
    """
    class __inner(object):
        def __init__(self, f):
            self.f = f
            update_wrapper(self, f)
            spooler_functions[self.__name__] = self

        def __call__(self, *args, **kwargs):
            if kwargs.pop("spool", True):
                from kb14 import init_database
                try:
                    init_database()
                    self.f(*args, **kwargs)
                except:
                    return uwsgi.SPOOL_RETRY
                return uwsgi.SPOOL_OK
            try:
                self.f(kwargs)
            except AutoReconnect:
                self.spool(*args, **kwargs)

        def perform(self, *args, **kwargs):
            return self.f(kwargs)

        def spawn(self, *args, **kwargs):
            kwargs.update(spool=False)
            gevent.spawn(self, **kwargs)

        def spool(self, *args, **kwargs):
            kwargs.update(ud_spool_func=self.__name__)
            uwsgi.mule_msg(json.dumps(kwargs))

    return __inner(f)


__all__ = ["job"]
