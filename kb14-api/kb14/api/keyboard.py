#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from flask import Blueprint, abort, request, jsonify

from kb14.api import missing, specify
from kb14.backends.key import Key
from kb14.backends.keyboard import Keyboard
from kb14.jobs.keyboard import add_key


keyboard = Blueprint("keyboard", __name__)


@keyboard.route("/keyboards", methods=["GET"])
def get_keyboards():
    return jsonify(data=[k._data for k in Keyboard.list()])


@keyboard.route("/keyboard/<color>", methods=["GET"])
def get_keyboard(color):
    keyboard = Keyboard.get(color) or missing("keyboard")
    return jsonify(keyboard._data)


@keyboard.route("/keyboard/<color>/keys", methods=["GET"])
def get_keyboard_keys(color):
    keyboard = Keyboard.get(color) or missing("keyboard")
    data = [{"date": k.date, "name": k.name} for k in keyboard.get_keys()]
    return jsonify(data=data)


@keyboard.route("/keyboard/<color>/key/<name>", methods=["GET"])
def get_keyboard_key(color, name):
    keyboard = Keyboard.get(color) or missing("keyboard")
    key = keyboard.get_key(name) or missing("key")
    return jsonify(data=key)


@keyboard.route("/keyboard", methods=["POST"])
def post_keyboard():
    json = request.get_json() or specify("keyboard color")
    color = json.get("color") or specify("keyboard color")
    keyboard = Keyboard(color=color)
    if keyboard.exists:
        abort(401, "A {} keyboard is already registered.".format(color))
    keyboard.save()
    return jsonify(keyboard._data)


@keyboard.route("/keyboard/<color>/key", methods=["POST"])
def post_keyboard_key(color):
    json = request.get_json() or specify("key name")
    name = json.get("name") or specify("key name")
    add_key.spawn(name=name, keyboard=color)
    Key.update_metrics(name=name, keyboard=color)
    return jsonify(name=name, keyboard=color)


__all__ = ["keyboard", "get_keyboards", "get_keyboards", "get_keyboard_keys",
           "get_keyboard_key", "post_keyboard", "post_keyboard_key"]
