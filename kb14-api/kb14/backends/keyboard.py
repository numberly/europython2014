#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from mongoengine import Document
from mongoengine.fields import StringField


class Keyboard(Document):
    color = StringField(required=True, unique=True, primary_key=True)

    def add_key(self, name):
        from kb14.backends.key import Key
        key = Key(name=name, keyboard=self)
        key.save(force_insert=True)
        return key

    def get_key(self, name, **kwargs):
        return [k.date for k in self.get_keys(name=name, **kwargs)]

    def get_keys(self, **kwargs):
        from kb14.backends.key import Key
        limit = kwargs.pop("limit", 100)
        kwargs.update({"keyboard": self.color})
        return list(Key.objects(**kwargs).order_by("-_id")[:limit])

    @property
    def exists(self):
        return (self.list(color=self.color) != [])

    @classmethod
    def list(cls, **kwargs):
        limit = kwargs.pop("limit", 100)
        return list(cls.objects(**kwargs)[:limit])

    @classmethod
    def get(cls, color, **kwargs):
        kwargs.update({"color": color})
        return cls.objects(**kwargs).first()


__all__ = ["Keyboard"]
