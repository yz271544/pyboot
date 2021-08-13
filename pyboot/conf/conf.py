#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: conf.py
@author: etl
@time: Created on 8/13/21 2:00 PM
@env: Python @desc:
@ref: @blog:
"""



class BaseConfig:
    app_name: str = ''
    description: str = ''


    def __repr__(self):
        return "%s(name=%r, description=%r)" % (self.__class__.name, self.name, self.description)

    def keys(self):
        """
        当对实例化对象使用dict(obj)的时候, 会调用这个方法,这里定义了字典的键, 其对应的值将以obj['name']的形式取,
        但是对象是不可以以这种方式取值的, 为了支持这种取值, 可以为类增加一个方法
        :return:
        """
        return ('name', 'description')

    def __getitem__(self, item):
        """
        内置方法, 当使用obj['name']的形式的时候, 将调用这个方法, 这里返回的结果就是值
        :param item:
        :return:
        """
        return getattr(self, item)
