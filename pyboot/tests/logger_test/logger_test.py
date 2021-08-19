#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: logger_test.py
@author: etl
@time: Created on 8/19/21 1:44 PM
@env: Python @desc:
@ref: @blog:
"""
import pytest
import logging


@pytest.mark.base
def test_logger_level():
    level = getattr(logging, "INFO", logging.DEBUG)
    print(level)
    assert 20 == level

