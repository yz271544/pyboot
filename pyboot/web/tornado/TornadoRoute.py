#!/usr/bin/env python
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: TornadoRoute.py
@author: etl
@time: Created on 8/17/21 5:08 PM
@env: Python @desc:
@ref: @blog:
"""
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('hello world!')


