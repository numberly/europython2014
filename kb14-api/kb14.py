#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

from kb14 import init_config, init_application, init_database
init_config("config.py")
init_database()
app = init_application()
