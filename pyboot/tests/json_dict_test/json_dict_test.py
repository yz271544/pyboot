#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: json_dict_test.py
@author: etl
@time: Created on 11/23/21 4:34 PM
@env: Python @desc:
@ref: @blog:
"""

import pytest
import json


@pytest.mark.base
def test_json_dict():
    data = """{
    "deviceInfo":{
        "deviceName":"设备3",
        "edgeDeviceName":"设备three",
        "topic":"GG2",
        "edgeCalculation":false,
        "encryption":false,
        "compression":false
    },
    "telemetry":{
        "ts":1585194439000,
        "RC_cylinder1_1P_d_dispPeak":86,
        "OPC温度":10370,
        "OPC湿度":"86",
        "OPC电量":true
    },
    "model_data":{
        "window":"short",
        "trend_model_data":[
            [
                1585298907056,
                33
            ],
            [
                1585298909060,
                33
            ],
            [
                1585298909266,
                33
            ]
        ]
    }
}"""
    dd = {}
    try:
        dd = json.loads(data)
        print(dd)
        print(dd["model_data"]["window"])
    except Exception:
        pass

    print(dd)


