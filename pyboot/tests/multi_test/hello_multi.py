#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: hello_multi.py
@author: etl
@time: Created on 8/19/21 9:08 AM
@env: Python @desc:
@ref: @blog:
"""
import time
import threading
from multiprocessing import Process


def sub_thread(i):
    print(f"i am sub thread for {i}")
    time.sleep(10)


def sub_process(i):
    print(f"i am sub_process_{i}")
    reading_thread = threading.Thread(target=sub_thread, args=(i,))
    reading_thread.daemon = True
    reading_thread.start()
    time.sleep(15)


if __name__ == '__main__':
    for i in range(3):
        p = Process(target=sub_process, args=(i, ))
        p.daemon = True
        p.start()
    time.sleep(20)

