#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from bson import ObjectId, DBRef
from flask.json import JSONEncoder as FlaskJSONEncoder
from mongoengine import Document


class JSONEncoder(FlaskJSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, DBRef) or isinstance(o, Document):
            return str(o.id)
        return super(JSONEncoder, self).default(o)


__all__ = ["JSONEncoder"]
