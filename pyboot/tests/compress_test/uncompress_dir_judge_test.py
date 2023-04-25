#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: uncompress_dir_judge_test.py
@author: lyndon
@time: Created on 2023/4/25 下午1:09
@env: Python 
@desc:
@ref: 
@blog:
"""
import pytest

from pyboot.utils.common.compress_utils import up_file_from_just_one_dir, move_up_files


@pytest.mark.base
def test_multi_files():
    origin_target_dir = "/lyndon/iProject/pypath/pyboot/pyboot/modules/gridsum/science/multivariate/Ch1hQGGkxnSAIiFrAAO8COz2yGE652"
    up_file_from_just_one_dir(origin_target_dir)

@pytest.mark.base
def test_just_one_directory():
    origin_target_dir = "/lyndon/iProject/pypath/pyboot/pyboot/modules/gridsum/science/multivariate"
    up_file_from_just_one_dir(origin_target_dir)
