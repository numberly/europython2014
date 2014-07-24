#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import uwsgi

from datetime import datetime
from mongoengine import Document
from mongoengine.fields import StringField, DateTimeField, ReferenceField

from kb14.backends.keyboard import Keyboard


class Key(Document):
    name = StringField(required=True)
    keyboard = ReferenceField(Keyboard, required=True)
    date = DateTimeField(default=datetime.now())

    @classmethod
    def list(cls, **kwargs):
        limit = kwargs.pop("limit", 100)
        return list(cls.objects(**kwargs).order_by("-_id")[:limit])

    @staticmethod
    def update_metrics(name, keyboard):
        uwsgi.metric_inc("application.keyboards.{}.{}".format(keyboard, name), 1)
        uwsgi.metric_inc("application.keyboards.{}.all".format(keyboard), 1)
        uwsgi.metric_inc("application.keyboards.all.{}".format(name), 1)
        uwsgi.metric_inc("application.keyboards.all.all", 1)


__all__ = ["Key"]
