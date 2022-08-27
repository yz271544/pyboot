#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
module to say hi
"""
import json
import os
import sys
import pickle

import numpy as np


def handler(event, context):
    # X_test = np.array([[event["t"], event["h"]]])
    # y_pred = test(X_test)
    # event['result'] = str(y_pred[0])
    event["test"] = "1234"
    return event


# def test(X_test):
#     # X_test = np.random.random((1000, 20))
#     with open(os.path.dirname(os.path.abspath(__file__)) + "/test.model", "rb") as f:
#         m = pickle.load(f)
#         y_pred = m.predict(X_test)
#     return y_pred


# def test_from_dict(event):
#     if isinstance(event, dict):
#         # print("dict:", event)
#         pass
#     elif isinstance(event, str):
#         print(event)
#         event = json.loads(s=event)
#     else:
#         print("Unknown:", type(event))
#         return
#
#     X_test = np.array([[event["t"], event["h"]]])
#     # X_test = np.random.random((1, 2))
#     a = None
#     try:
#         y_pred = test(X_test)
#         a = str(y_pred[0])
#     except UserWarning as e:
#         pass
#     # print("result:", a)
#     return a


if __name__ == "__main__":
    # argv_ = sys.argv[1]
    # print(argv_)
    # event = {}
    # event["t"] = 40
    # event["h"] = 50
    # X_test = np.array([[event["t"], event["h"]]])
    # # X_test = np.random.random((1, 2))
    # y_pred = test(X_test)
    # a = str(y_pred[0])
    # print("result:", a)

    # test_from_dict(event)

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
    ddd = json.loads(data)
    print(ddd)
    ccc = handler(ddd, None)
    print(ccc)
