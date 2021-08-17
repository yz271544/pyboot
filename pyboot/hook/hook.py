#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: hook.py
@author: etl
@time: Created on 8/17/21 6:29 PM
@env: Python @desc:
@ref: @blog:
"""
import signal

from pyboot.logger import log
from pyboot.starter import BaseStarter, GetStarters
from pyboot.starter_context import StarterContext


class HookStarter(BaseStarter):
    def __init__(self):
        self.callbacks = []

    def sig_handler(self, starter_context: StarterContext):
        log.info("start sig_handler")
        for fn in self.callbacks:
            fn(starter_context)

    def Init(self, starter_context: StarterContext):
        for starter in GetStarters():
            log.debug("starter name:%s", starter.__class__.__name__)
            self.callbacks.append(starter.Stop)
        return

    def Setup(self, starter_context: StarterContext):
        signal.signal(signal.SIGINT, lambda: self.sig_handler(starter_context))
        signal.signal(signal.SIGTERM, lambda: self.sig_handler(starter_context))
        return

    def Start(self, starter_context: StarterContext):
        return

    def Stop(self, starter_context: StarterContext):
        return