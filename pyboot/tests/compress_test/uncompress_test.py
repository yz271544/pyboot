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
import os
import re
from pathlib import Path
from pyboot.utils.common.compress_utils import un_zip, un_gz, un_tar


class UnCompressTest(unittest.TestCase):

    def test_uncompress_zip(self):
        src_full_zip_file = "/lyndon/iProject/pypath/pyboot/pyboot/modules/gridsum/science/Csg8EmGdnIyAVJdVAAHaY0adxNc829.zip"
        un_zip(src_full_zip_file, "/tmp/model_test_target_dir")

    def test_un_gz(self):
        src_full_gz_file = "/home/etl/cps/cps-gateway-data-access-5.3.7.tar.gz"
        un_gz(src_full_gz_file, "/tmp/model_test_target_dir")

    def test_un_tar_gz(self):
        src_full_gz_file = "/home/etl/cps/cps-gateway-data-access-5.3.7.tar.gz"
        un_gz(src_full_gz_file, "/tmp/model_test_target_dir")
        un_tar("/tmp/model_test_target_dir/cps-gateway-data-access-5.3.7.tar", "/tmp/model_test_target_dir")

    def test_path(self):
        path1 = "/home/etl/bbb"
        path2 = "/fff"
        print(os.path.basename(path2))
        print(os.path.join(path1, os.path.basename(path2)))

    def test_splitext(self):
        file_name = 'cps-gateway-data-access-5.3.7.tar.gz'
        print(os.path.splitext(file_name))

    def test_pathlib(self):
        file_name = 'cps-gateway-data-access-5.3.7.tar.gz'
        print(Path(file_name).suffix)

    def test_re_tar_gz(self):
        re_regex = r".*.tar.gz$"
        file_name = '/tmp/abcd/cps-gateway-data-access-5.3.7.tar.gz'
        match = re.match(re_regex, file_name)
        if match:
            print("true")
        else:
            print("false")
        print("dirName:", os.path.dirname(file_name))
        print("baseName:", os.path.basename(file_name))
        file_name_tuple = os.path.splitext(os.path.basename(file_name))
        print(file_name_tuple[0])
        print(file_name_tuple[1])


