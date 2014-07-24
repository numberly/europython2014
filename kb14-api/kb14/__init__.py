#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import mongoengine

from flask import Flask, jsonify
from werkzeug.exceptions import (
    default_exceptions, HTTPException, InternalServerError
)

from kb14.api.key import key
from kb14.api.keyboard import keyboard
from kb14.utils.encoder import JSONEncoder


app = Flask(__name__)


def make_errors_json(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    response = jsonify(code=e.code, message=e.description)
    response.status_code = e.code
    return response


def init_config(filename):
    app.config.from_pyfile("../{}".format(filename))


def init_database():
    mongoengine.connect(db=app.config.get("MONGO_DB_NAME", "kb14"),
                        host=app.config.get("MONGO_HOST", "localhost"),
                        port=app.config.get("MONGO_PORT", 27017))


def init_application():
    app.register_blueprint(keyboard, url_prefix="/api")
    app.register_blueprint(key, url_prefix="/api")
    for code in default_exceptions.keys():
        app.register_error_handler(code, make_errors_json)
    app.json_encoder = JSONEncoder
    return app


__all__ = ["init_config", "init_database", "init_application"]
