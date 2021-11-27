#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: model_dynamic_import_test.py
@author: etl
@time: Created on 11/26/21 8:33 AM
@env: Python @desc:
@ref: @blog:
"""

import os
import unittest
import importlib
import json
from pyboot.conf.settings import MODEL_PATH, PYBOOT_HOME, MODEL_REF_PREFIX


class ModelDynamicImportTest(unittest.TestCase):

    def test_os_path_sep(self):
        print("os.path.pathsep: %s" % os.path.pathsep)
        print("os.path.sep: %s" % os.path.sep)
        print("os.sep: %s" % os.sep)
        print("os.altsep: %s" % os.altsep)
        print("os.linesep: %s" % os.linesep)
        print("os.extsep: %s" % os.extsep)

        # Linux Output:
        # os.path.pathsep: :
        # os.path.sep: /
        # os.sep: /
        # os.altsep: None
        # os.linesep:
        #
        # os.extsep: .

    def test_base_importlib(self):
        pkg_path = os.path.join(MODEL_REF_PREFIX, "trend_threshold/index")

        if pkg_path[0] == os.sep:
            pkg_path = pkg_path[1:]

        print("pkg_path: %s" % pkg_path)
        slist = str(pkg_path).split(os.sep)
        pkg_name = '.'.join(slist)
        #     return '.'.join(slist[:-1]), slist[-1]

        print("pkg_name: %s" % pkg_name)

        test_data_file = os.path.join(PYBOOT_HOME, "tests/test_data/theshld.json")
        print("test_data_file: %s" % test_data_file)
        with open(test_data_file, 'r') as f:
            test_data = f.read()
            # print(test_data)
            dict_test_data = json.loads(test_data)

        print(dict_test_data)
        model_module = importlib.import_module(pkg_name)
        ret = model_module.handler(dict_test_data, None)
        print("ret: %s" % ret)

    def test_base_importlib_zd(self):
        pkg_path = os.path.join(MODEL_REF_PREFIX, "thend_threshold_zd/index")

        if pkg_path[0] == os.sep:
            pkg_path = pkg_path[1:]

        print("pkg_path: %s" % pkg_path)
        slist = str(pkg_path).split(os.sep)
        pkg_name = '.'.join(slist)
        #     return '.'.join(slist[:-1]), slist[-1]

        print("pkg_name: %s" % pkg_name)

        test_data_file = os.path.join(PYBOOT_HOME, "tests/test_data/theshld.json")
        print("test_data_file: %s" % test_data_file)
        with open(test_data_file, 'r') as f:
            test_data = f.read()
            # print(test_data)
            dict_test_data = json.loads(test_data)

        print(dict_test_data)
        model_module = importlib.import_module(pkg_name)
        ret = ""
        try:
            ret = model_module.handler(dict_test_data, None)
        except Exception as e:
            ret = "Exception: %r" % e
        print("ret: %r" % ret)



