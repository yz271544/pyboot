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

from pyboot.logger.plogging import FormatKey


@pytest.mark.base
def test_logger_level():
    level = getattr(logging, "INFO", logging.DEBUG)
    print(level)
    assert 20 == level


@pytest.mark.base
def test_log_format():
    # fmt = FormatKey.log_format(FormatKey.supported_keys)
    print(FormatKey.simple_format_info)
    print(FormatKey.supported_format)
