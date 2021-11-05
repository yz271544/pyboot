#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: base_test.py
@author: etl
@time: Created on 8/17/21 11:14 PM
@env: Python @desc:
@ref: @blog:
"""
import pytest

test_dict = {}
test_list = []


class BaseClazz(object):

    def __init__(self):
        pass

    def Init(self, starter_context):
        return

    def Setup(self, starter_context):
        return


@pytest.mark.base
def test_class_name1():
    ba1 = BaseClazz()
    print(ba1.__class__.__name__)


@pytest.mark.base
def test_for_range():
    sa = 2
    for i in range(sa):
        print("i ---> ", i)


@pytest.mark.base
def test_type_dict():
    dd = {"dic": "m"}
    print(type(dd))
    print(type(dd) == dict)
    print("dic" in dd)


"""
pytest -s -m "base" pyboot/tests/base_test/base_test.py::test_type_collect_init
"""
@pytest.mark.base
def test_type_collect_init():
    if not bool(test_dict):
        print("test_dict is None")
        test_dict['a'] = 1
    else:
        print("test_dict is not None")
        print(test_dict)

    if not bool(test_dict):
        print("test_dict is None")
    else:
        print("test_dict is not None")
        print(test_dict)

    if not bool(test_list):
        print("test_dict is None")
        test_list.append(1)
    else:
        print("test_list is not None")
        print(test_list)

    if not bool(test_list):
        print("test_list is None")
    else:
        print("test_list is not None")
        print(test_list)

