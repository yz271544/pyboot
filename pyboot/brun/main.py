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
from pyboot.conf import getBaseConf
from pyboot.logger import log

if __name__ == '__main__':
    confArr = getBaseConf()
    for conf in confArr:
        log.info("conf:{%s}", conf)

    log.info("brun main")
