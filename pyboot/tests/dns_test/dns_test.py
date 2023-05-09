#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: dict_base_test.py
@author: etl
@time: Created on 8/17/21 1:02 PM
@env: Python @desc:
@ref: @blog:
"""
import pytest
import socket


@pytest.mark.base
def test_resolver_1():
    addrs = socket.getaddrinfo('www.baidu.com', 80)
    print(addrs)


@pytest.mark.base
def test_resolver_2():
    addrs = socket.gethostbyname('www.baidu.com')
    print(addrs)


@pytest.mark.base
def test_resolver_3():
    myaddr = socket.getaddrinfo('www.baidu.com', 'http')
    print(myaddr[0][4][0])


@pytest.mark.base
def test_resolver_4():
    try:
        addrs = socket.gethostbyname('www.baidu')
        print(addrs)
    except Exception as e:
        print("resolve failed:" + str(e))

