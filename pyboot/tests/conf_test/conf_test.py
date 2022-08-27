#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: conf_test.py
@author: etl
@time: Created on 8/18/21 2:45 PM
@env: Python @desc:
@ref: @blog:
"""
import json
import os

import pytest
import yaml

import pyboot.conf as pybootconf
from pyboot.conf import FuncSchema


@pytest.mark.skip("和现在的设计不符合")
def test_load_from_yaml():
    baseConf = pybootconf.get_base_conf()
    edge1 = baseConf.edge[0]
    packName, funcName = edge1.edge_mode_package()
    print("PackageName:", packName)
    print("FuncName:", funcName)


@pytest.mark.base
def test_split_from_str():
    ss = "pyboot.modules.gridsum.science.industry.telemetry.telm_temperature"
    slist = ss.split('.')
    print("PackageName:", '.'.join(slist[:-1]))
    print("FuncName:", slist[-1])


@pytest.mark.base
def test_format_str():
    print(r"PackageName:%s" % "abc")
    print("PackageName:{pkgName}".format(pkgName="abc"))
    funName = "testFunc"
    print(f"FuncName:{funName}")


@pytest.mark.base
def test_load_check_funcs():
    with open("/lyndon/iProject/pypath/pyboot/pyboot/conf/config.yaml", 'r', encoding='utf-8') as cf:
        cnf = yaml.load(cf.read(), Loader=yaml.FullLoader)
        func_schema = FuncSchema(many=True)
        funcs = func_schema.dump(cnf['funcs'])
        print(json.dumps(funcs))

@pytest.mark.base
def test_get_env_bool():
    from distutils.util import strtobool
    a = "False"
    print(strtobool(a))
    b = True
    print(b)
