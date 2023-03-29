#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: load_test.py
@author: lyndon
@time: Created on 2023/3/29 下午6:25
@env: Python 
@desc:
@ref: 
@blog:
"""
import os
import sys
import time
import traceback
import pytest
import joblib

@pytest.mark.base
def test_logger_level():
    """
    Pickle depends on the module path. So, should make sure that the module index.py is in sys.path.
    """
    index_path = "/lyndon/iProject/pypath/pyboot/pyboot/modules/gridsum/science/multivariate/index.py"

    dir_name = os.path.dirname(index_path)
    print("dir_name:", dir_name)
    if dir_name not in sys.path:
        sys.path.append(dir_name)

    init_path = "/lyndon/iProject/pypath/pyboot/pyboot/modules/gridsum/science/multivariate/903378b4-6b75-45ba-8ed2-d0f2c6a3e130.model"
    model = joblib.load(init_path, 'r')
    print("multivariate_feature:", model.multivariate_feature)
    print("threshold:", model.threshold)
    print("model", model.model)


