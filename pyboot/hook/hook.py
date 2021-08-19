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
        log.info("HookStarter Init Begin")
        for starter in GetStarters():
            log.debug("starter name:%s", starter.__class__.__name__)
            self.callbacks.append(starter.Stop)

        log.info(f"HookStarter callback length:{len(self.callbacks)}")

        log.info("HookStarter Init End")
        return

    def Setup(self, starter_context: StarterContext):
        log.info("HookStarter Setup Begin")
        signal.signal(signal.SIGINT, lambda x, y: self.sig_handler(starter_context))
        signal.signal(signal.SIGTERM, lambda x, y: self.sig_handler(starter_context))
        log.info("HookStarter Setup End")
        return

    def Start(self, starter_context: StarterContext):
        log.info("HookStarter Start Begin")
        log.info("HookStarter Start End")
        return

    def Stop(self, starter_context: StarterContext):
        log.info("HookStarter Stop Begin")
        log.info("HookStarter Stop End")
        return
