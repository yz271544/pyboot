 #!/usr/bin/env python
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: pickle_test.py
@author: etl
@time: Created on 11/23/21 8:30 PM
@env: Python @desc:
@ref: @blog:
"""

import pytest
import pickle


@pytest.mark.base
def test_parse_pickle():
    file = "/lyndon/iProject/pypath/pyboot/pyboot/modules/gridsum/science/multivar/a9885e6d-bbcc-4bce-be3d-de310affe351.model"

    p = pickle.load(file)
    print(p)


