#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: WebValidator.py
@author: etl
@time: Created on 8/17/21 4:57 PM
@env: Python @desc:
@ref: @blog:
"""

# 结构体指针检查验证，如果传入的interface为nil，就通过log.Panic函数抛出一个异常
# 被用在starter中检查公共资源是否被实例化了
from pyboot.logger import log


def Check(a):
	if a is None:
		log.critical("object can't be None")

