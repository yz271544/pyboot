#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: model_record_test.py
@author: etl
@time: Created on 11/25/21 3:17 PM
@env: Python @desc:
@ref: @blog:
"""
import unittest

from pyboot.conf import EdgeFuncConfig
from pyboot.utils.model.record import ModelRecord


class ModelRecordTest(unittest.TestCase):

    def test_init_record(self):
        model_record = ModelRecord()
        self.assertEqual(len(model_record.model_record_dict), 0)

    def test_add_record(self):
        # multivar_dev2_OPCtemperature###fafdafjadskfasfadfasf
        f = {
            "modelAddress": "http://10.200.60.18:9000/group1/M00/01/0D/Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip",
            "modelMd5": "fafdafjadskfasfadfasf",
            "modelName": "multivar_dev2_OPCtemperature",
            "devices": [
                {
                    "device": [
                        {
                            "attrName": "deviceName",
                            "attrValue": "三厂-pyboot测试设备",
                            "attrExpression": "== data_to_dict['deviceInfo']['deviceName']"
                        },
                        {
                            "attrName": "pointName",
                            "attrValue": "pyboot",
                            "attrExpression": "in data_to_dict['telemetry']"
                        }
                    ]
                }
            ]
        }
        func = EdgeFuncConfig(**f)
        model_record = ModelRecord()
        # model_record._add(func)
        # self.assertEqual(len(model_record.model_record_dict), 1)
        judge = model_record.determine(func)
        print(judge)
        model_record.truncate()
        print(len(model_record.model_record_dict))

    def test_determine_new_record(self):
        # multivar_dev2_OPCtemperature###fafdafjadskfasfadfasf
        f = {
            "model_address": "http://10.200.60.18:9000/group1/M00/01/0D/Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip",
            "model_md5": "fffff",
            "modelName": "multivar_dev2_OPCxxxx",
            "devices": [
                {
                    "device": [
                        {
                            "attrName": "deviceName",
                            "attrValue": "三厂-pyboot测试设备",
                            "attrExpression": "== data_to_dict['deviceInfo']['deviceName']"
                        },
                        {
                            "attrName": "pointName",
                            "attrValue": "pyboot",
                            "attrExpression": "in data_to_dict['telemetry']"
                        }
                    ]
                }
            ]
        }
        func = EdgeFuncConfig(**f)
        model_record = ModelRecord()
        judge = model_record.determine(func)
        print(judge)
        model_record.truncate()
        print(len(model_record.model_record_dict))

    def test_determine_new_records(self):
        # multivar_dev2_OPCtemperature###fafdafjadskfasfadfasf
        f1 = {
            "model_address": "http://10.200.60.18:9000/group1/M00/01/0D/Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip",
            "model_md5": "fffff",
            "modelName": "multivar_dev2_OPCxxxx",
            "devices": [
                {
                    "device": [
                        {
                            "attrName": "deviceName",
                            "attrValue": "三厂-pyboot测试设备",
                            "attrExpression": "== data_to_dict['deviceInfo']['deviceName']"
                        },
                        {
                            "attrName": "pointName",
                            "attrValue": "pyboot",
                            "attrExpression": "in data_to_dict['telemetry']"
                        }
                    ]
                }
            ]
        }
        func1 = EdgeFuncConfig(**f1)

        f2 = {
            "model_address": "http://10.200.60.18:9000/group1/M00/01/0D/Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip",
            "model_md5": "fafdafjadskfasfadfasf",
            "modelName": "multivar_dev2_OPCtemperature",
            "devices": [
                {
                    "device": [
                        {
                            "attrName": "deviceName",
                            "attrValue": "三厂-pyboot测试设备",
                            "attrExpression": "== data_to_dict['deviceInfo']['deviceName']"
                        },
                        {
                            "attrName": "pointName",
                            "attrValue": "pyboot",
                            "attrExpression": "in data_to_dict['telemetry']"
                        }
                    ]
                }
            ]
        }
        func2 = EdgeFuncConfig(**f2)

        funcs = [func1, func2]

        model_record = ModelRecord()
        for func in funcs:
            judge = model_record.determine(func)
            print(judge)
        model_record.truncate()
        print(len(model_record.model_record_dict))

    def test_determine_duplicate_records(self):
        # multivar_dev2_OPCtemperature###fafdafjadskfasfadfasf
        f1 = {
            "model_address": "http://10.200.60.18:9000/group1/M00/01/0D/Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip",
            "model_md5": "fffff",
            "modelName": "multivar_dev2_OPCxxxx",
            "devices": [
                {
                    "device": [
                        {
                            "attrName": "deviceName",
                            "attrValue": "三厂-pyboot测试设备",
                            "attrExpression": "== data_to_dict['deviceInfo']['deviceName']"
                        },
                        {
                            "attrName": "pointName",
                            "attrValue": "pyboot",
                            "attrExpression": "in data_to_dict['telemetry']"
                        }
                    ]
                }
            ]
        }
        func1 = EdgeFuncConfig(**f1)

        f2 = {
            "model_address": "http://10.200.60.18:9000/group1/M00/01/0D/Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip",
            "model_md5": "fafdafjadskfasfadfasf",
            "modelName": "multivar_dev2_OPCtemperature",
            "devices": [
                {
                    "device": [
                        {
                            "attrName": "deviceName",
                            "attrValue": "三厂-pyboot测试设备",
                            "attrExpression": "== data_to_dict['deviceInfo']['deviceName']"
                        },
                        {
                            "attrName": "pointName",
                            "attrValue": "pyboot",
                            "attrExpression": "in data_to_dict['telemetry']"
                        }
                    ]
                }
            ]
        }
        func2 = EdgeFuncConfig(**f2)

        f3 = {
            "model_address": "http://10.200.60.18:9000/group1/M00/01/0D/Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip",
            "model_md5": "ggggg",
            "modelName": "multivar_dev2_OPCxxxx",
            "devices": [
                {
                    "device": [
                        {
                            "attrName": "deviceName",
                            "attrValue": "三厂-pyboot测试设备",
                            "attrExpression": "== data_to_dict['deviceInfo']['deviceName']"
                        },
                        {
                            "attrName": "pointName",
                            "attrValue": "pyboot",
                            "attrExpression": "in data_to_dict['telemetry']"
                        }
                    ]
                }
            ]
        }
        func3 = EdgeFuncConfig(**f3)

        funcs = [func1, func2, func3]

        model_record = ModelRecord()
        for func in funcs:
            judge = model_record.determine(func)
            print(judge)
        print(len(model_record.model_record_dict))
        # clean
        model_record.truncate()
        print(len(model_record.model_record_dict))
