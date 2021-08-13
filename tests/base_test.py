#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: base_test.py
@author: etl
@time: Created on 8/13/21 12:33 PM
@env: Python @desc:
@ref: @blog:
"""
import sys
import unittest


class BaseTest(unittest.TestCase):

    def test_max_int(self):
        INT_MAX = int(0 >> 1)
        print(INT_MAX)

        i = sys.maxsize
        print(i)

    def test_list_append(self):
        a1 = [1, 2, 3, 4]
        a2 = [5, 6, 7, 8]
        a = a1 + a2
        print(a)
