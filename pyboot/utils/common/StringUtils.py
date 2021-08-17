#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: StringUtils.py
@author: lyndon
@time: Created on 2021-01-15 14:14
@env: Python
@desc:
@ref:
@blog:
"""


class StringUtils:
    splitFlag = ","

    @staticmethod
    def mkstring_start_end(origin_str, start_with_str, end_with_str):
        """
        :argument: origin_str:abc
        :argument: start_with_str:(
        :argument: end_with_str:)
        :return: (abc)
        """
        return start_with_str + origin_str + end_with_str

    @staticmethod
    def mkstring_bracket(origin_str, brackets_str):
        """
        :param origin_str: abc
        :param brackets_str: "
        :return: "abc"
        """
        return StringUtils.mkstring_start_end(origin_str, brackets_str, brackets_str)

    @staticmethod
    def mkstring_collect_start_end(collection, start_with_str, end_with_str, split_flag="") -> str:
        """
        :param collection:["a", "b", "c"]
        :param start_with_str: (
        :param end_with_str: )
        :param split_flag: ,
        :return: (a),(b),(c)
        """
        collLen = len(collection)
        if collLen == 1:
            return start_with_str + collection[0] + end_with_str
        else:
            collection = map(lambda x: start_with_str + x + end_with_str, collection)
            return split_flag.join(collection)

    @staticmethod
    def mkstring_collect_bracket(collection, brackets_str, split_flag):
        """
        :param collection: ["a", "b", "c"]
        :param brackets_str: '
        :param split_flag: ,
        :return: 'a','b','c'
        """
        return StringUtils.mkstring_collect_start_end(collection, brackets_str, brackets_str, split_flag)

    @staticmethod
    def replace_by_dict(origin_str, _dict):
        """
        :param origin_str: (abc && cde)
        :param _dict: {"abc": "select XXX", "cde": "select YYY"}
        :return: (select XXX && select YYY)
        """
        for k, v in _dict.items():
            origin_str = StringUtils.replaceAll(origin_str, k, v)
        return origin_str
        # for k, v in _dict.items():
        #     origin_str = origin_str.replace(k, v)
        # return origin_str

    @staticmethod
    def dict_zip(key, value, splitFlag=splitFlag):
        """
        :param key: a,b
        :param value: 1,2
        :param splitFlag: ,
        :return: {'a': '1', 'b': '2'}
        """
        keySlice = key.split(splitFlag)
        valueSlice = value.split(splitFlag)
        return dict(zip(keySlice, valueSlice))

    @staticmethod
    def replaceAll(input: str, toReplace: str, replaceWith: str):
        while (input.find(toReplace) > -1):
            input = input.replace(toReplace, replaceWith)
        return input


if __name__ == '__main__':
    a1 = "a"
    print(StringUtils.mkstring_bracket(a1, "'"))

    print(StringUtils.mkstring_start_end(a1, "(", ")"))

    arr1 = ["a", "b", "c"]
    print(StringUtils.mkstring_collect_bracket(arr1, "'", ","))

    print(StringUtils.mkstring_collect_start_end(arr1, "(", ")", ","))

    arr2 = ["a"]
    print(StringUtils.mkstring_collect_bracket(arr2, "'", ","))

    print(StringUtils.mkstring_collect_start_end(arr2, "(", ")", ","))

    a2 = "(abc && cde)"

    m2 = {"abc": "select XXX", "cde": "select YYY"}

    # for m, mv in m2.items():
    #     # print(m, mv)
    #     a2 = a2.replace(m, mv)

    a2 = StringUtils.replace_by_dict(a2, m2)

    print(a2)

    m3 = {"&&": " and ", "||": " or "}

    a2 = StringUtils.replace_by_dict(a2, m3)

    print(a2)

    key = "a,b"
    value = "1,2"
    d = StringUtils.dict_zip(key, value)
    print(d)

    formula_exp = "x >= a AND x < b"
    formula_exp = StringUtils.replaceAll(formula_exp, "x", "ORDER_DATE")
    formula_exp = StringUtils.replaceAll(formula_exp, "a", "20201201")
    formula_exp = StringUtils.replaceAll(formula_exp, "b", "20201231")

    print(formula_exp)

