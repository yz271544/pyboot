#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: Generator.py
@author: lyndon
@time: Created on 2021-01-17 21:27
@env: Python
@desc:
@ref:
@blog:
"""

from pyboot.utils.common.JsonUtils import JsonUtils
from pyboot.utils.common.SnowflakeId import IdWorker
from pyboot.utils.common.StringUtils import StringUtils


class Generator:


    # 类型简称key必须是唯一的，且不能为各个value字串的子串，否则导致无线循环
    # data_type = {
    #     "CH": "STRING",  # 字符串类型
    #     "DT": "STRING",  # 日期类型
    #     "MP": "STRING",  # 地图类型
    #     "NV": "DECIMAL(14,2)",  # 数值类型
    #     "IT": "INT",  # 整形
    #     "DC": "DECIMAL(14,2)"  # 数值类型
    # }
    # data_type = DataTypeOfDataCenterSwitch(DATACENTER_DB_TYPE).get()

    logic_dict = {
        "&&": " and ",
        "||": " or "
    }

    def __init__(self):
        self.idWorker = IdWorker()

    def generate_by_id(self, id):
        generate_tasks = self.generate()
        return generate_tasks

    def generate(self):
        # custmGrpBasInfoList = self.custmGrpBasInfoService.getByStatus(0)
        generate_tasks = []
        return generate_tasks

