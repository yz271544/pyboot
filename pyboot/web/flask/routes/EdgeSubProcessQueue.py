#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: EdgeSubProcessQueue.py
@author: etl
@time: Created on 8/19/21 2:36 PM
@env: Python @desc:
@ref: @blog:
"""
from pyboot import web
from pyboot.core.MqttProcessor import MqttProcessor
from pyboot.utils.common.web.BaseController import BaseController
from pyboot.utils.error.Errors import EgonException


@web.webApp.route('/queue_size_metrics')
def subprocess_performance_overstock():
    queue_size_metrics = {}
    try:
        queue_size = MqttProcessor.query_queue_size()
        queue_size_metrics["queue_size_metrics"] = queue_size
    except Exception as e:
        we = EgonException(f"query subprocess queue size failed:{e}")
        queue_size_metrics["error"] = we

    return BaseController().json(queue_size_metrics)

