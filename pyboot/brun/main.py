#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: main.py
@author: etl
@time: Created on 8/17/21 1:44 PM
@env: Python @desc:
@ref: @blog:
"""
from pyboot.brun import starterRegister
from pyboot.boot import BootApplication
from pyboot.conf import getBaseConf
from pyboot.logger import log
from pyboot.starter_context import StarterContext

if __name__ == '__main__':
    # confArr = getBaseConf()
    # for conf in confArr:
    #     log.info("conf:{%s}", conf)
    baseConf = getBaseConf()

    log.info("brun main")

    startContext = StarterContext().SetProps(baseConf)

    # app = BootApplication(False, startContext, starterRegister)
    app = BootApplication(False, startContext)
    app.Start()
