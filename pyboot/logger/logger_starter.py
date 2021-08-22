#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: logger_starter.py
@author: etl
@time: Created on 8/22/21 10:17 AM
@env: Python @desc:
@ref: @blog:
"""
from pyboot.conf.base_conf_starter import Props
from pyboot.logger import Plog
from pyboot.starter import BaseStarter
from pyboot.starter_context import StarterContext


class LoggerStarter(BaseStarter):
    def Init(self, starter_context: StarterContext):
        props = Props()
        Plog.update_log_props(props)
        return

    def Setup(self, starter_context: StarterContext):
        return

    def Start(self, starter_context: StarterContext):
        return

    def Stop(self, starter_context: StarterContext):
        return
