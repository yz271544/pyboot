#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: EdgeSubProcessQueue.py
@author: etl
@time: Created on 8/19/21 12:45 PM
@env: Python @desc:
@ref: @blog:
"""
import tornado.web

from pyboot.core.MqttProcessor import MqttProcessor
from pyboot.utils.error.Errors import EgonException


class EdgeSubProcessQueue(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        queue_size_metrics = {}
        try:
            queue_size = MqttProcessor.query_queue_size()
            queue_size_metrics["queue_size_metrics"] = queue_size
        except Exception as e:
            we = EgonException(f"query subprocess queue size failed:{e}")
            queue_size_metrics["error"] = we

        self.write(queue_size_metrics)
