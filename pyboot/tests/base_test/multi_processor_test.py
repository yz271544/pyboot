#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: multi_processor_test.py
@author: etl
@time: Created on 8/18/21 6:20 PM
@env: Python @desc:
@ref: @blog:
"""


import multiprocessing
import time


def worker(interval):
    print("work start:{0}".format(time.ctime()))
    time.sleep(interval)
    print("work end:{0}".format(time.ctime()))


if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
    p.daemon = True
    p.start()
    # p.join()
    print("start!")
    time.sleep(5)
    print("end!")
