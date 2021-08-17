#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: dict_base_test.py
@author: etl
@time: Created on 8/17/21 1:02 PM
@env: Python @desc:
@ref: @blog:
"""
import pytest

from pyboot.utils.error.Errors import EgonException

KeyProps = "_conf"

@pytest.mark.base
def test_dict_none():
    context = {}
    print(context is None)
    with pytest.raises(EgonException):
        try:
            p = context[KeyProps]
            print("p:", p)
        except:
            raise EgonException("配置还没有被初始化")


@pytest.mark.base
def test_dict_default():
    context = {
        "testing": True
    }
    context.setdefault('testing', True)
    print(context.get('testing'))
    assert True == context.get('testing'), "Error testing isn't True"