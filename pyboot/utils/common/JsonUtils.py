#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: JsonUtils.py
@author: lyndon
@time: Created on 2021-01-17 22:13
@env: Python
@desc:
@ref:
@blog:
"""
import json


class JsonUtils:
    @staticmethod
    def obj_to_json(obj):
        return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def json_to_obj(typ, json_str):
        dict_info = json.loads(s=json_str)
        attrs = typ.init_attrs()
        obj = typ(*attrs)
        obj.__dict__ = dict_info
        return obj

    @staticmethod
    def list_to_json(lis):
        return json.dumps(lis)

    @staticmethod
    def json_to_list(list_json):
        return json.loads(list_json)

    @staticmethod
    def dict_to_json(dic):
        return json.dumps(dic)

    @staticmethod
    def json_to_dict(dict_json):
        return json.loads(dict_json)


class TestStudent:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def student2dict(self):
        return {
            'name': self.name,
            'age': self.age
        }

    @staticmethod
    def init_attrs():
        return "", 0


if __name__ == '__main__':
    ts = TestStudent("huzy", 10)
    js = JsonUtils.obj_to_json(ts)
    print(js)

    obj = JsonUtils.json_to_obj(TestStudent, js)
    print(obj.name)
    print(obj.age)

    # myClassReBuild = json.loads(js)
    # print(myClassReBuild)
    # myClass2 = TestStudent("", 0)
    # # 将字典转化为对象
    # myClass2.__dict__ = myClassReBuild
    # print(myClass2.name)
    # print(myClass2.age)

    # l = ["a", "b", "c"]
    # ljson = json.dumps(l)
    # print(ljson)
    # ljson2 = JsonUtils.obj_to_json(l)
    # print(ljson2)
    #
    # print("=========================")
    # lStr = """["a", "b", "c"]"""
    # ll = json.loads(lStr)
    # print(ll)
    # print(ll[:2])
    #
    # print("===============")
    # dic = {"a": 1, "b": 2}
    # dJson = json.dumps(dic)
    # print(dJson)
    #
    # dStr = """{"a": 1, "b": 2}"""
    # dd = json.loads(dStr)
    # print(dd)
    # print(dd["a"])
    # print(dd["b"])



