#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: __init__.py.py
@author: etl
@time: Created on 8/17/21 1:39 PM
@env: Python @desc:
@ref: @blog:
"""
from pyboot.utils.common import WebValidator

webApp = None


def WebApp():
    WebValidator.Check(webApp)
    return webApp
