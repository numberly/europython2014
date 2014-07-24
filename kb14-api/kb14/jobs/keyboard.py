#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from kb14.utils.decorators import job


@job
def add_key(message):
    from kb14.backends.keyboard import Keyboard
    color = message.get("keyboard", None)
    if color is None:
        return
    keyboard = Keyboard.get(color)
    if keyboard is None:
        return
    keyboard.add_key(message.get("name", None))
    return


__all__ = ["add_key"]
