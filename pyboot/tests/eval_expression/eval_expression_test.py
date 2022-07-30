#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: eval_expression_test.py
@author: lyndon
@time: Created on 2022/7/29 下午6:17
@env: Python 
@desc:
@ref: 
@blog:
"""
import unittest
import json
from jsonpath_ng import jsonpath, parse


class EvalExpression(unittest.TestCase):

    data = """
        {
            "deviceInfo":{
                "deviceName":"三厂-pyboot测试设备",
                "edgeDeviceName":"设备three",
                "topic":"GG2",
                "edgeCalculation":false,
                "encryption":false,
                "compression":false
            },
            "telemetry":{
                "ts":1585194439000,
                "RC_cylinder1_1P_d_dispPeak":86,
                "pyboot":10370
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
        }
        """

    def test_simple_eval(self):
        exp = """print("abc test 123")"""
        eval(exp)
        exec(exp)

    def test_return_val(self):
        print(eval("1 > 0"))
        print(eval("0 > 1"))

    def test_json_parser(self):
        # print(parse("$").find(data))

        # print(parse("$.deviceInfo").find(data))
        json_data = json.loads(self.data)

        device_name = "init value"
        try:
            device_name = eval("json_data['deviceInfo']['deviceName']")
        except SyntaxError as e:
            print("device parser expression syntax error" + e.msg)

        print(device_name)

        # print(json_data)
        print(parse("$.deviceInfo.deviceName").find(json_data))
        print(parse(r"$.deviceInfo.deviceName").find(json_data))
        print(parse("""$.deviceInfo.deviceName""").find(json_data))

        # print(parse("""$.deviceInfo.?deviceName='三厂-pyboot测试设备'""").find(json_data))