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
from pyboot.conf import get_base_conf
from pyboot.logger import log
from pyboot.starter_context import StarterContext

if __name__ == '__main__':

    baseConf = get_base_conf()

    log.info("brun main")

    startContext = StarterContext().SetProps(baseConf)

    app = BootApplication(False, startContext)
    app.Start()
