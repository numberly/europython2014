#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify

from kb14.api import missing
from kb14.backends.key import Key


key = Blueprint("key", __name__)


@key.route("/keys", methods=["GET"])
def get_keys():
    data = [{"date": k.date, "keyboard": k.keyboard, "name": k.name}
            for k in Key.list()]
    return jsonify(data=data)


@key.route("/key/<name>", methods=["GET"])
def get_key(name):
    data = [{"date": k.date, "keyboard": k.keyboard}
            for k in Key.list(name=name)] or missing("key")
    return jsonify(data=data)


__all__ = ["key", "get_keys", "get_key"]
