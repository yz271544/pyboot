#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: block_test.py
@author: etl
@time: Created on 8/19/21 11:17 AM
@env: Python @desc:
@ref: @blog:
"""
from queue import Empty

import pytest
from multiprocessing import Queue


@pytest.mark.base
def test_no_block_by_queue():
    q = Queue()
    while True:
        try:
            q.get(block=False)
        except Empty as e:
            pass


@pytest.mark.base
def test_block_by_queue():
    print("block_by_queue")
    q = Queue()
    while True:
        try:
            q.get(block=True)
        except Empty as e:
            pass


@pytest.mark.base
def test_block_by_queue_timeout():
    print("block_by_queue_timeout")
    q = Queue()
    while True:
        try:
            q.get(block=True, timeout=5)
        except Empty as e:
            pass
        except Exception as ex:
            print(ex)

