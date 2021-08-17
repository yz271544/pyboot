#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: signal_src.py
@author: etl
@time: Created on 8/17/21 7:27 PM
@env: Python @desc:
@ref: @blog:
"""

import os
import signal

# 发送信号，16175是前面那个绑定信号处理函数的pid，需要自行修改
os.kill(28134, signal.SIGTERM)
# 发送信号，16175是前面那个绑定信号处理函数的pid，需要自行修改
# os.kill(28134, signal.SIGUSR1)
