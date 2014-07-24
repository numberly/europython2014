#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from flask import abort


def specify(what):
    abort(400, "You must specify the {}.".format(what))


def missing(what):
    abort(404, "Unknown {}.".format(what))


__all__ = ["specify", "missing"]
