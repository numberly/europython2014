#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""We need this mule because we can't uwsgi.spool in a greenlet.

To resolve this problem, we send a message from the greenlet to the mule (that
IS part of the uWSGI stack, not only having the context), that itself transmits
the message on the spool.
"""
import ast
import uwsgi

while True:
    message = uwsgi.mule_get_msg()
    if message:
        message = ast.literal_eval(message)
        uwsgi.spool(message)
