#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: list_test.py
@author: etl
@time: Created on 8/17/21 4:24 PM
@env: Python @desc:
@ref: @blog:
"""
import pytest


@pytest.mark.base
def test_append_list():
    lst = []
    lst.append(1)
    lst.append(2)
    print(lst)



# class A:
#     def __init__(self):
#         self.l1 = []
#         self.l2 = []
#
#     def
#