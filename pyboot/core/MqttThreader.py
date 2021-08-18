#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: MqttThreader.py
@author: etl
@time: Created on 8/18/21 1:10 PM
@env: Python @desc:
@ref: @blog:
"""
import importlib
import threading
from queue import Queue

from paho.mqtt.packettypes import PacketTypes

from pyboot.core.MqttClient import MqttClient
from pyboot.logger import log
from pyboot.utils.error.Errors import UnknownArgNum

MAX_QUEUE = 1000
TIME_OUT = 120
MAX_EDGE_NUM = 10


class MqttThreader:

    def __init__(self, pre_broker: str, pre_port: int, pre_topic: str, pre_qos: int, post_broker: str, post_port: int,
                 post_topic: str, post_qos: int, edge_model_pkg_name, edge_model_func_name):
        self.pre_queue = Queue(maxsize=MAX_QUEUE)
        self.pre_broker = pre_broker
        self.pre_port = pre_port
        self.pre_topic = pre_topic
        self.pre_qos = pre_qos
        self.post_queue = Queue(maxsize=MAX_QUEUE)
        self.post_broker = post_broker
        self.post_port = post_port
        self.post_topic = post_topic
        self.post_qos = post_qos
        self.edge_model_pkg_name = edge_model_pkg_name
        self.edge_model_func_name = edge_model_func_name
        self.edge_model_func = self.load_edge_model(self.edge_model_pkg_name, self.edge_model_func_name)

    def load_edge_model(self, pkgName, funcName):
        module = importlib.import_module(pkgName)
        if hasattr(module, funcName):
            return getattr(module, funcName)
        else:
            raise UnknownArgNum(f"Unable to found the corresponding package {pkgName} or func:{funcName}")

    def pre_threader(self, pre_queue):
        def pre_on_message(client, userdata, msg):
            message = msg.payload
            try:
                pre_queue.put(message, block=True, timeout=TIME_OUT)
            except Exception as e:
                log.debug(f"put msg to the pre_queue Exception:{e}, queue:{pre_queue.qsize()}")

        mqtt_client = MqttClient(self.pre_broker, self.pre_port, self.pre_topic, self.pre_qos, PacketTypes.SUBSCRIBE,
                                 on_message=pre_on_message)
        try:
            mqtt_client.run_consumer()
        except Exception as e:
            log.debug(f"consume mqtt failed!{e}")
            pass

    def post_threader(self):
        mqtt_client = MqttClient(self.post_broker, self.post_port, self.post_topic, self.post_qos,
                                 PacketTypes.PUBLISH)
        while True:
            data = None
            try:
                data = self.post_queue.get(block=True, timeout=TIME_OUT)
            except Exception as e:
                log.debug(f"get from the pre_queue Exception:{e}, queue:{self.post_queue.qsize()}")
                pass

            try:
                mqtt_client.run_publish(data)
            except Exception as e:
                log.debug(f"publish mqtt failed:{e}")
                pass

    def edge_model_calc(self, i):
        while True:
            in_data = None
            out_data = None
            try:
                in_data = self.pre_queue.get(block=True, timeout=TIME_OUT)
            except Exception as e:
                log.debug(f"get msg from pre_queue Exception:{i} - {e}, queue:{self.pre_queue.qsize()}")

            if in_data is not None:
                out_data = self.edge_model_func(in_data)

            if out_data is not None:
                try:
                    self.post_queue.put(out_data, block=True, timeout=TIME_OUT)
                except Exception as e:
                    log.debug(f"put msg to the post_queue Exception:{i} - {e}, queue:{self.post_queue.qsize()}")

    def make_thead(self):
        reading_thread = threading.Thread(target=self.pre_threader, args=(self.pre_queue,))
        reading_thread.daemon = True
        writing_thread = threading.Thread(target=self.post_threader)
        writing_thread.daemon = True
        reading_thread.start()
        writing_thread.start()
        for i in range(MAX_EDGE_NUM):
            edge_model_thread = threading.Thread(target=self.edge_model_calc, args=(i,))
            edge_model_thread.daemon = True
            edge_model_thread.start()

