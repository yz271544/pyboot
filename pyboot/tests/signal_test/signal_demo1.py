#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: signal_demo1.py
@author: etl
@time: Created on 8/17/21 7:22 PM
@env: Python @desc:
@ref: @blog:
"""

''''' 
子进程结束会向父进程发送SIGCHLD信号 
'''
import pytest
import os
import signal
from time import sleep


def onsigchld(a, b):
    print('收到子进程结束信号')


@pytest.mark.base
def test_signal_demo1():
    signal.signal(signal.SIGCHLD, onsigchld)

    pid = os.fork()
    if pid == 0:
        print('我是子进程,pid是', os.getpid())
        sleep(2)
    else:
        print('我是父进程,pid是', os.getpid())
        os.wait()  # 等待子进程结束
