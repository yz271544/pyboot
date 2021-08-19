#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: BaseController
@author: lyndon
@time: Created on 2021-01-22 12:56
@env: Python
@desc:
@ref:
@blog:
"""

from flask import jsonify
from pyboot.utils.common.web.Code import Code


class BaseController:
    '''
    * 返回Json数据
    * @param  dict body
    * @return json
    '''

    @staticmethod
    def json(body=None):
        if body is None:
            body = {}
        return jsonify(body)

    '''
    * 返回错误信息
    * @param  msg string
    * @return json
    '''

    def error(self, msg='', show=True):
        return self.json({'code': Code.BAD_REQUEST, 'error': True, 'msg': msg, 'show': show})

    '''
    * 返回成功信息
    * @param  msg string
    * @return json
    '''

    def successData(self, data='', msg='', show=True):
        return self.json({'code': Code.SUCCESS, 'data': data, 'msg': msg, 'show': show})
