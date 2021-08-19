#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: Index.py
@author: etl
@time: Created on 8/19/21 2:48 PM
@env: Python @desc:
@ref: @blog:
"""
from pyboot import web
from pyboot.utils.common.web.BaseController import BaseController


@web.webApp.route('/')
def index():
    return BaseController().successData('hello world!')
