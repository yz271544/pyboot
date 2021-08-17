#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: __init__.py.py
@author: etl
@time: Created on 8/17/21 1:44 PM
@env: Python @desc:
@ref: @blog:
"""
from pyboot.logger import log
from pyboot.starter import Register
from pyboot.conf.base_conf_starter import BaseConfStarter
from pyboot.web.tornado.tornado_server import TornadoServer

log.info("brun __init__ start")
Register(BaseConfStarter())
Register(TornadoServer())
log.info("brun __init__ end")
