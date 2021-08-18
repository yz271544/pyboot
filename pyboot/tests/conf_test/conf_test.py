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
import pytest
import pyboot.conf as pybootconf


@pytest.mark.base
def test_load_from_yaml():
    baseConf = pybootconf.getBaseConf()
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

