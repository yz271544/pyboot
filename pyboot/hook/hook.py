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

from pyboot.starter import BaseStarter
from pyboot.starter_context import StarterContext


class HookStarter(BaseStarter):
    def __init__(self):
        self.callbacks = []

    def sig_handler(self):
        # for starter in
        pass

    def Init(self, starter_context: StarterContext):
        signal.signal(signal.SIGINT, self.sig_handler)
        signal.signal(signal.SIGTERM, self.sig_handler)




        # signal.signal(signal.SIGINT, sig_handler)
        #
        #
        # signal.Notify(sigs, syscall.SIGQUIT, syscall.SIGTERM)
        # go func()
        # {
        # for {
        #     c := < -sigs
        # log.Info("notify: ", c)
        # for _, fn := range callbacks {
        # fn()
        # }
        # break
        # os.Exit(0)


        return

    def Setup(self, starter_context: StarterContext):
        return

    def Start(self, starter_context: StarterContext):
        return

    def Stop(self, starter_context: StarterContext):
        return