#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo1.py
@author: etl
@time: Created on 8/17/21 9:40 PM
@env: Python @desc:
@ref: @blog:
"""

# encoding:utf-8
__author__ = 'Fioman'
__time__ = '2019/3/6 13:36'
import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with Singleton._instance_lock:
                if not hasattr(cls, '_instance'):
                    Singleton._instance = super().__new__(cls)

            return Singleton._instance


obj1 = Singleton()
obj2 = Singleton()
print(obj1, obj2)

print("========================================================")

def task(arg):
    obj = Singleton()
    print(obj)


for i in range(10):
    t = threading.Thread(target=task, args=[i, ])
    t.start()
