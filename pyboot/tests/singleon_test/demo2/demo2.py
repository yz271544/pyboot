#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo2.py
@author: etl
@time: Created on 8/17/21 9:42 PM
@env: Python @desc:
@ref: @blog:
"""
# encoding:utf-8
__author__ = 'Fioman'
__time__ = '2019/3/6 11:38'

import time
import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        time.sleep(1)

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(Singleton, '_instance'):
            with Singleton._instance_lock:
                if not hasattr(Singleton, '_instance'):
                    Singleton._instance = Singleton(*args, **kwargs)

        return Singleton._instance


def task(arg):
    obj = Singleton.get_instance(arg)
    print(obj)


for i in range(10):
    t = threading.Thread(target=task, args=[i, ])
    t.start()

obj = Singleton.get_instance()
print(obj)
