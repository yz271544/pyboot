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
from pyboot.hook.hook import HookStarter
from pyboot.logger.logger_starter import LoggerStarter
from pyboot.processors.processor_starter import ProcessorStarter
from pyboot.starter import StarterRegister
from pyboot.conf.base_conf_starter import BaseConfStarter
# from pyboot.web.tornado.tornado_server import TornadoServer
from pyboot.web.flask.flask_server import FlaskStarter

starterRegister = StarterRegister()
starterRegister.Register(BaseConfStarter())
starterRegister.Register(LoggerStarter())
starterRegister.Register(ProcessorStarter())
# starterRegister.Register(TornadoServer())
starterRegister.Register(FlaskStarter())
starterRegister.Register(HookStarter())
