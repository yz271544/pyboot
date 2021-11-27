#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: uncompress_test.py
@author: etl
@time: Created on 11/25/21 2:25 PM
@env: Python @desc:
@ref: @blog:
"""
import unittest

from pyboot.utils.common.compress_utils import un_zip


class UnCompressTest(unittest.TestCase):

    def test_uncompress_zip(self):
        src_full_zip_file = "/lyndon/iProject/pypath/pyboot/pyboot/modules/gridsum/science/Csg8EmGdnIyAVJdVAAHaY0adxNc829.zip"
        un_zip(src_full_zip_file, "/tmp/model_test_target_dir")


