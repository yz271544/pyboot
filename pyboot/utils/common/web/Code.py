#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: Code
@author: lyndon
@time: Created on 2021-01-22 12:56
@env: Python
@desc:
@ref:
@blog:
"""


class Code:
    SUCCESS = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    ERROR = 500

    ERROR_AUTH_CHECK_TOKEN_FAIL    = 10001
    ERROR_AUTH_CHECK_TOKEN_TIMEOUT = 10002
    ERROR_AUTH_TOKEN               = 10003
    ERROR_AUTH                     = 10004