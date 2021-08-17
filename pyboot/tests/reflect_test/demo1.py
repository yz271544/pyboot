#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo1.py
@author: etl
@time: Created on 8/17/21 7:41 PM
@env: Python @desc:
@ref: @blog:
"""
import pytest
import sys
import importlib


@pytest.mark.base
def test_reflect_mod1_func1():
    # print(sys.modules['pyboot.modules.mod1'])
    mod1 = importlib.import_module('pyboot.modules.mod1.mod1')
    print(getattr(mod1, 'func1')())


