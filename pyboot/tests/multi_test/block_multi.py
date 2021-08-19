#!/usr/bin/env python
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: block_multi.py
@author: etl
@time: Created on 8/19/21 10:20 AM
@env: Python @desc:
@ref: @blog:
"""
import time
import threading
from multiprocessing import Process, Queue
from queue import Queue as tQueue

TIME_OUT = 120


def sub_thread(i):
    print(f"i am sub thread for {i}")
    time.sleep(10)


def sub_process(i, queue):
    print(f"i am sub_process_{i}")
    reading_thread = threading.Thread(target=sub_thread, args=(i,), name=f"sub_process_{i}_thread_1")
    reading_thread.daemon = True
    reading_thread.start()
    while True:
        main_msg = queue.get(block=True, timeout=TIME_OUT)
        if main_msg is None:
            break
        elif type(main_msg) == dict and "msg" in main_msg:
            print("msg:", main_msg)
            queue.put("world", block=True, timeout=TIME_OUT)
        else:
            print(main_msg)


if __name__ == '__main__':
    q_list = []
    p_list = []
    for i in range(3):
        q = Queue(1000)
        p = Process(target=sub_process, args=(i, q, ), name=f"sub_process_{i}")
        p.daemon = True
        p.start()
        q_list.append(q)
        p_list.append(p)
    time.sleep(12)
    msg = {"msg": "hello"}
    q1 = q_list[0]
    q1.put(msg, block=True, timeout=TIME_OUT)
    while True:
      q1_msg = q1.get(block=True, timeout=TIME_OUT)
      print(q1_msg)
      if q1_msg == "world":
          break


