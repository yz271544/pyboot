#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: index.py.py
@author: etl
@time: Created on 8/18/21 2:09 PM
@env: Python @desc:
@ref: @blog:
"""
import random


def telm_body_len(payload):
    return len(payload)


def telm_temperature(payload):
    temp = random.randint(40, 80)
    if isinstance(payload, dict):
        payload["temperature"] = temp
        return payload
    else:
        ret = {
            "temperature": temp,
            "payload": payload,
        }
        return ret


def handler(event, context):
    telm_temperature(event)
    return event


if __name__ == '__main__':
    m1 = "test_1234"
    p1 = telm_body_len(m1)
    print(p1)

    m2 = "test_5678"
    p2 = telm_temperature(m2)
    print(p2)

    m3 = {"msg": "test_7890"}
    p3 = telm_temperature(m3)
    print(p3)

    m4 = {"msg": "success", "code": 200,
          "data": {"name": "lyndon", "books": 500, "mary": True, "children": ["nn", "jy"]}}
    p4 = telm_temperature(m4)
    print(p4)

    p5 = handler(m4, None)
    print(p5)
