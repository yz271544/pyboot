#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: MqttProcessor.py
@author: etl
@time: Created on 8/18/21 4:11 PM
@env: Python @desc:
@ref: @blog:
"""
import os
from multiprocessing import Process

from pyboot.conf.config import EdgeModelConfig
from pyboot.core.MqttThreader import MqttThreader
from pyboot.logger import log
from pyboot.utils.error.Errors import EgonException


class MqttProcessor:

    def __init__(self, edges):
        self.edges = edges

    def process_maker(self, edge: EdgeModelConfig, i: int):
        print('id %d, %s is running, parent id is [%s]' % (i, os.getpid(), os.getppid()))
        edge_model_conf = edge
        print(f'edge_model_conf:{edge_model_conf}')
        edge_model_pkg_name, edge_model_func_name = edge_model_conf.edge_mode_package()

        try:
            mqtt_threader = MqttThreader(edge_model_conf.pre_broker, edge_model_conf.pre_port,
                                         edge_model_conf.pre_topic, edge_model_conf.pre_qos,
                                         edge_model_conf.post_broker, edge_model_conf.post_port,
                                         edge_model_conf.post_topic, edge_model_conf.post_qos,
                                         edge_model_pkg_name, edge_model_func_name)
            mqtt_threader.make_run_thead()
        except Exception as e:
            log.error(f"make and run the mqtt threader is failed.{e}")
            pass

    def process(self):
        if self.edges is None:
            raise EgonException("the edge config is None, please check the config.yaml")

        # 单进程测试使用
        # for edge in self.edges:
        #     edge_model_conf = edge
        #     for i in range(edge_model_conf.instance):
        #         print('主:', os.getpid(), os.getppid(), i)
        #         self.process_maker(edge_model_conf, i,)

        print('主', os.getpid(), os.getppid())
        for edge in self.edges:
            edge_model_conf = edge
            for i in range(edge_model_conf.instance):
                p = Process(target=self.process_maker, args=(edge_model_conf, i,))
                p.daemon = True
                p.start()

