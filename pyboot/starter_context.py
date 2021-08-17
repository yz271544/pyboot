#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: starter_context.py
@author: etl
@time: Created on 8/13/21 1:47 PM
@env: Python @desc:
@ref: @blog:
"""

from attrdict import AttrDict

from pyboot.utils.error.Errors import EgonException

KeyProps = "_conf"


class AliasedAttrDict(AttrDict):
    context = {}

    def __getitem__(self, key):
        if key in self.__class__.context:
            return super(AliasedAttrDict, self).__getitem__(self.__class__.context[key])
        return super(AliasedAttrDict, self).__getitem__(key)

    def __getattr__(self, key):
        if key in self.__class__.context:
            return super(AliasedAttrDict, self).__getitem__(self.__class__.context[key])
        return super(AliasedAttrDict, self).__getitem__(key)


class StarterContext(AliasedAttrDict):
    context = {}

    def Props(self):
        try:
            p = self.context[KeyProps]
            return p
        except:
            raise EgonException("配置还没有被初始化")

    def SetProps(self, conf):
        self.context[KeyProps] = conf


if __name__ == '__main__':
    d = StarterContext({"tower": "Babel", "floor": "Dirty", "pos": (0, 0)})
    print(d.tower)
    print(d.floor)
    print(d.pos)
