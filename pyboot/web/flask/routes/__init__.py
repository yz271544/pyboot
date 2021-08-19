#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: __init__.py.py
@author: etl
@time: Created on 8/19/21 2:29 PM
@env: Python @desc:
@ref: @blog:
"""


def init_app(app):
    from pyboot.web.flask.routes.EdgeSubProcessQueue import subprocess_performance_overstock
    from pyboot.web.flask.routes.Index import index
    print("--- init routes ---")
    print(app.url_map)
