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
import time
from multiprocessing import Process, Queue

from pyboot.conf.config import EdgeModelConfig
from pyboot.conf.settings import SUB_PROCESS_BLOCK, SUB_PROCESS_TIMEOUT
from pyboot.core.MqttThreader import MqttThreader
from pyboot.logger import log
from pyboot.utils.error.Errors import EgonException


class MqttProcessor:
    q_list = []
    p_list = []

    def __init__(self, edges):
        self.edges = edges

    def process_maker(self, edge: EdgeModelConfig, sub_process_name: str, queue: Queue):
        log.info('%s [%s] is running, parent id is [%s]' % (os.getpid(), sub_process_name, os.getppid()))
        edge_model_conf = edge
        # print(f'edge_model_conf:{edge_model_conf}')
        edge_model_pkg_name, edge_model_func_name = edge_model_conf.edge_mode_package()

        try:
            mqtt_threader = MqttThreader(sub_process_name,
                                         edge_model_conf.pre_broker, edge_model_conf.pre_port,
                                         edge_model_conf.pre_topic, edge_model_conf.pre_qos,
                                         edge_model_conf.post_broker, edge_model_conf.post_port,
                                         edge_model_conf.post_topic, edge_model_conf.post_qos,
                                         edge_model_pkg_name, edge_model_func_name)
            mqtt_threader.make_run_thead()
            while True:
                main_msg = queue.get(block=SUB_PROCESS_BLOCK, timeout=None)
                if main_msg is None:
                    log.info("get msg None")
                    mqtt_threader.join_thread_from_box()
                    break
                elif type(main_msg) == dict and "qsize" in main_msg:
                    log.info("msg:", main_msg)
                    res_qsize_msg = mqtt_threader.query_queue_size()
                    queue.put(res_qsize_msg, block=SUB_PROCESS_BLOCK, timeout=SUB_PROCESS_TIMEOUT)
                else:
                    log.info(main_msg)
        except Exception as e:
            log.error(f"make and run the mqtt threader is failed.{e}")
            pass
        print("---------------------- process_maker ---------------------------------")

    def process(self):
        if self.edges is None:
            raise EgonException("the edge config is None, please check the config.yaml")

        # 单进程测试使用
        # for edge in self.edges:
        #     edge_model_conf = edge
        #     for i in range(edge_model_conf.instance):
        #         print('主:', os.getpid(), os.getppid(), i)
        #         self.process_maker(edge_model_conf, i,)
        # print("---------------------- 单进程测试使用 ---------------------------------")

        # print('主', os.getpid(), os.getppid())

        for edge in self.edges:
            edge_model_conf = edge
            for i in range(edge_model_conf.instance):
                q = Queue()
                process_name = f"sub_process_{edge_model_conf.name}_{i}"
                p = Process(target=self.process_maker, args=(edge_model_conf, process_name, q),
                            name=process_name)
                p.daemon = True
                self.q_list.append(q)
                self.p_list.append(p)
                p.start()
        # print("---------------------- 多进程测试使用 ---------------------------------")

    @classmethod
    def query_queue_size(cls):
        queue_size = []
        query_queue_size_msg = {"qsize": 0}
        for q in cls.q_list:
            try:
                q.put(query_queue_size_msg, block=True, timeout=2)
            except Exception as e:
                log.error(f"send query qsize failed:{e}")

        for q in cls.q_list:
            try:
                res_queue_size_msg = q.get(block=True, timeout=2)
                queue_size.append(res_queue_size_msg)
            except Exception as e:
                log.error(f"get qsize response failed:{e}")

        return queue_size

    @classmethod
    def teardown(cls):
        log.info("try send close msg to the subprocess")
        for q in cls.q_list:
            try:
                q.put(None, block=True, timeout=2)
                time.sleep(1)
            except Exception as e:
                log.error(f"send teardown msg failed:{e}")
        log.info("try join the subprocess")
        for p in cls.p_list:
            p.join()
