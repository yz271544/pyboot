#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: Errors.py
@author: lyndon
@time: Created on 2021-01-19 9:35
@env: Python
@desc:
@ref:
@blog:
"""


class ApplicationError(Exception):
    def __init__(self, cause, trace):
        self.cause = cause
        self.trace = trace

    def __str__(self):
        return '{origin}\nFrom {parent}'.format(origin=self.trace,
                                                parent=self.cause)


class EgonException(BaseException):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '<%s>' % self.msg


class UnknownFieldType(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '<%s>' % self.msg


class UnknownArgNum(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '<%s>' % self.msg


class TypeMappingError(BaseException):
    def __init__(self, ErrorInfo):
        # super().__init__(self)  # 初始化父类
        self.message = ErrorInfo

    def __str__(self):
        return self.message


class TableNotExistsError(BaseException):
    def __init__(self, ErrorInfo):
        # super().__init__(self)  # 初始化父类
        self.message = ErrorInfo

    def __str__(self):
        return self.message


class SystemUnknownError(BaseException):
    def __init__(self, ErrorInfo):
        # super().__init__(self)  # 初始化父类
        self.message = ErrorInfo

    def __str__(self):
        return self.message