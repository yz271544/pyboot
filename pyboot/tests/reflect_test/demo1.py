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


@pytest.mark.base
def test_reflect_gridsum_science_industry_telm1():
    telemetry = importlib.import_module('pyboot.modules.gridsum.science.industry.telemetry')
    body_len = getattr(telemetry, 'telm_body_len')(
        "can signify a number of emotions including but not limited to distress, anger, amazement, joy, \
        disbelief, confusion, dumbfoundedness, fear, and despair.")
    assert body_len == 160


@pytest.mark.base
def test_reflect_gridsum_science_industry_telm2():
    telemetry = importlib.import_module('pyboot.modules.gridsum.science.industry.telemetry')
    body = getattr(telemetry, 'telm_temperature')(
        {"msg": "success", "code": 200,
          "data": {"name": "lyndon", "books": 500, "mary": True, "children": ["nn", "jy"]}})
    print(body)
    assert isinstance(body, dict)
    assert body.__contains__("temperature")

