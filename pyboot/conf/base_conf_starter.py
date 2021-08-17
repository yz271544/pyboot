#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: base_conf_starter.py
@author: etl
@time: Created on 8/17/21 2:33 PM
@env: Python @desc:
@ref: @blog:
"""
from pyboot.logger import log
from pyboot.starter import BaseStarter
from pyboot.starter_context import StarterContext

global_conf = {}


def Props():
    return global_conf


class BaseConfStarter(BaseStarter):
    def Init(self, starter_context: StarterContext):
        log.info("BaseConfStarter Init start")
        global global_conf
        global_conf = starter_context.Props()
        log.info("初始化配置")
        log.info("BaseConfStarter Init end")
        return

