#!/usr/bin/env python
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: tornado_server.py
@author: etl
@time: Created on 8/17/21 2:23 PM
@env: Python @desc:
@ref: @blog:
"""
from pyboot.logger import log
from pyboot.starter import BaseStarter
from pyboot.starter_context import StarterContext


class TornadoServer(BaseStarter):

    def Init(self, starter_context: StarterContext):
        log.info("TornadoServer Init start")
        log.info("TornadoServer Init end")
        return

    def Setup(self, starter_context: StarterContext):
        return

    def Start(self, starter_context: StarterContext):
        return

    def Stop(self, starter_context: StarterContext):
        return

    def StartBlocking(self) -> bool:
        return True
