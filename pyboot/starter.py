#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: starter.py
@author: etl
@time: Created on 8/13/21 9:37 AM
@env: Python @desc:
@ref: @blog:
"""
import sys
# import functools
import threading
# from pyboot.core.core import Singleton
# from starter_context import StarterContext

SystemGroup = 30
BasicResourcesGroup = 20
AppGroup = 10

INT_MAX = sys.maxsize
DEFAULT_PRIORITY = 10000


class Starter:
    def Init(self, starter_context):
        return

    def Setup(self, starter_context):
        return

    def Start(self, starter_context):
        return

    def Stop(self, starter_context):
        return

    def PriorityGroup(self) -> int:
        return 0

    def StartBlocking(self) -> bool:
        return False

    def Priority(self) -> int:
        return 0


# 服务启动注册器
class StarterRegister:
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.nonBlockingStarters = []
        self.blockingStarters = []

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            with StarterRegister._instance_lock:
                if not hasattr(cls, '_instance'):
                    StarterRegister._instance = super().__new__(cls)

            return StarterRegister._instance

        # self.nonBlockingStarters = [Starter]
        # self.blockingStarters = [Starter]

    # 返回所有的启动器
    def AllStarters(self) -> []:
        starters = self.nonBlockingStarters + self.blockingStarters
        return starters

    # 注册启动器
    def Register(self, starter):
        if starter.StartBlocking():
            self.blockingStarters.append(starter)
        else:
            self.nonBlockingStarters.append(starter)


# StarterRegister = StarterRegister()
# Starters = [Starter]


# 注册starter
def Register(starter: Starter):
    StarterRegister().Register(starter)


#排序starter
# def SortStarters():
#     def cmp(a, b):
#         # 这个函数按照类Intervals的属性end降序排序
#         if a.PriorityGroup() > b.PriorityGroup():
#             return -1
#         if a.Priority() > b.Priority():
#             return 1
#         return 0
#
#     starters = sorted(Starters, key=functools.cmp_to_key(cmp))
#     return starters


# 获取所有注册的starter
def GetStarters() -> [Starter]:
    return StarterRegister().AllStarters()


# 默认的空实现,方便资源启动器的实现
class BaseStarter(Starter):
    def Init(self, starter_context):
        return

    def Setup(self, starter_context):
        return

    def Start(self, starter_context):
        return

    def Stop(self, starter_context):
        return

    def PriorityGroup(self) -> int:
        return BasicResourcesGroup

    def StartBlocking(self) -> bool:
        return False

    def Priority(self) -> int:
        return DEFAULT_PRIORITY
