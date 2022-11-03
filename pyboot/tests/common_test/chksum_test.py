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
import hashlib
from pyboot.utils.common.ChkSum import GetBase64Md5Byte, GetFileMd5Byte, get_md5_from_big_file, get_md5_from_small_file


@pytest.mark.base
def test_md5():
    target_file = "/home/etl/cps/bogusModel.rar"
    md5_value = GetFileMd5Byte(target_file)
    print(md5_value)
    sbm = GetBase64Md5Byte(md5_value)
    print(sbm)

@pytest.mark.base
def test_sys_md5():
    target_file = "/home/etl/cps/bogusModel.rar"
    sys_sbm = get_md5_from_big_file(target_file)
    print(sys_sbm)
