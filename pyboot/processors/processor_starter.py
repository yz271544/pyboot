#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: processor_starter.py
@author: etl
@time: Created on 8/18/21 6:27 PM
@env: Python @desc:
@ref: @blog:
"""
from pyboot.conf import BaseConfig
from pyboot.conf.base_conf_starter import Props
from pyboot.conf.settings import DOWNLOAD_MODEL
from pyboot.core.MqttProcessor import MqttProcessor
from pyboot.logger import log
from pyboot.starter import BaseStarter
from pyboot.starter_context import StarterContext
from pyboot.utils.model.model import download_by_funcs


class ProcessorStarter(BaseStarter):
    def __init__(self):
        self.props = None
        self.processor = None

    def Init(self, starter_context: StarterContext):
        log.info("ProcessorStarter Init start")
        props = Props()
        print(props.__class__.__name__) # BaseConfig
        self.props = props
        if DOWNLOAD_MODEL:
            download_by_funcs(self.props.funcs)
        log.info("初始化配置")
        log.info("ProcessorStarter Init end")
        return

    def Setup(self, starter_context):
        log.info("ProcessorStarter Setup Begin...")
        if self.props is not None and len(self.props.edge) > 0:
            self.processor = MqttProcessor(self.props.edge, self.props.funcs)
        log.info("ProcessorStarter Setup END...")
        return

    def Start(self, starter_context):
        log.info("ProcessorStarter Start Begin...")
        if self.processor is not None:
            self.processor.process()
        log.info("ProcessorStarter Start END...")
        return

    def Stop(self, starter_context):
        log.info("ProcessorStarter Stop Begin...")
        self.processor.teardown()
        log.info("ProcessorStarter Stop END...")


