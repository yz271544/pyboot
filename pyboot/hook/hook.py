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

from pyboot.starter import BaseStarter, GetStarters
from pyboot.starter_context import StarterContext


class HookStarter(BaseStarter):
    def __init__(self):
        self.callbacks = []

    def sig_handler(self, starter_context: StarterContext):
        # for starter in GetStarters():
        #     print("stop starter:", starter.__class__.name)
        #     starter.Stop(starter_context)
        for fn in self.callbacks:
            fn(starter_context)

    def Init(self, starter_context: StarterContext):
        for starter in GetStarters():
            self.callbacks.append(starter.Stop)
        return

    def Setup(self, starter_context: StarterContext):
        signal.signal(signal.SIGINT, lambda x: self.sig_handler(x))
        signal.signal(signal.SIGTERM, lambda x: self.sig_handler(x))
        return

    def Start(self, starter_context: StarterContext):
        return

    def Stop(self, starter_context: StarterContext):
        return