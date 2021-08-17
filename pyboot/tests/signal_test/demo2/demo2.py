#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: demo2.py
@author: etl
@time: Created on 8/17/21 7:29 PM
@env: Python @desc:
@ref: @blog:
"""

import os
import signal
from time import sleep
from queue import Queue

QCOUNT = Queue()  # 初始化队列


def onsigchld(a, b):
    '''''收到信号后向队列中插入一个数字1'''
    print('收到SIGUSR1信号')
    sleep(2)
    QCOUNT.put(1)  # 向队列中写入


def exithanddle(s, e):
    raise SystemExit('收到终止命令,退出程序')


signal.signal(signal.SIGUSR1, onsigchld)  # 绑定信号处理函数
signal.signal(signal.SIGINT, exithanddle)  # 当按下Ctrl + C 终止进程

while 1:
    print('我的pid是', os.getpid())
    print('现在队列中元素的个数是', QCOUNT.qsize())
    sleep(2)
