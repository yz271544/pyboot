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
