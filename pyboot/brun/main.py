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
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
# print(os.path.dirname(BASE_DIR))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
    
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
