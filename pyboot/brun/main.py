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
import pyboot.brun
from pyboot.boot import BootApplication
from pyboot.conf import getBaseConf
from pyboot.logger import log
from pyboot.starter_context import StarterContext

if __name__ == '__main__':
    confArr = getBaseConf()
    for conf in confArr:
        log.info("conf:{%s}", conf)

    log.info("brun main")

    app = BootApplication(False, confArr, StarterContext().SetProps(confArr))
    app.Start()
