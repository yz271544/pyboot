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
import os
import threading
import json
from queue import Queue

from paho.mqtt.packettypes import PacketTypes

from pyboot.conf import EdgeFuncConfig
from pyboot.conf.settings import MAX_QUEUE, TIME_OUT, MAX_EDGE_NUM, MODEL_REF_PREFIX, PYBOOT_HOME
from pyboot.core.MqttClient import MqttClient
from pyboot.logger import log
from pyboot.utils.error.Errors import UnknownArgNum

# MAX_QUEUE = 1000
# TIME_OUT = 120
# MAX_EDGE_NUM = 10


def edge_model_handle(model_name, in_data_dict):
    pkg_path = os.path.join(MODEL_REF_PREFIX, "%s/index" % model_name)

    if pkg_path[0] == os.sep:
        pkg_path = pkg_path[1:]

    # print("pkg_path: %s" % pkg_path)
    slist = str(pkg_path).split(os.sep)
    pkg_name = '.'.join(slist)

    # print("pkg_name: %s" % pkg_name)

    try:
        model_module = importlib.import_module(pkg_name)
        ret = model_module.handler(in_data_dict, None)
    except ModuleNotFoundError as mnfe:
        msg = f"No module pkg_name: {pkg_name}, {mnfe}"
        ret = msg
        log.error(msg)
    except Exception as e:
        msg = f"internal exception: {e}"
        ret = msg
        log.error(msg)
    return ret


class MqttThreader:

    def __init__(self, sub_process_name: str,
                 pre_broker_protocol: str,
                 pre_broker_host: str,
                 pre_port: int,
                 pre_topic: str,
                 pre_qos: int,
                 post_broker_protocol: str,
                 post_broker_host: str,
                 post_port: int,
                 post_topic: str,
                 post_qos: int,
                 funcs: [EdgeFuncConfig]):
                 # edge_model_pkg_name,
                 # edge_model_func_name):
        self.sub_process_name = sub_process_name
        self.pre_queue = Queue(maxsize=MAX_QUEUE)
        self.pre_broker_protocol = pre_broker_protocol
        self.pre_broker_host = pre_broker_host
        self.pre_port = pre_port
        self.pre_topic = pre_topic
        self.pre_qos = pre_qos
        self.post_queue = Queue(maxsize=MAX_QUEUE)
        self.post_broker_protocol = post_broker_protocol
        self.post_broker_host = post_broker_host
        self.post_port = post_port
        self.post_topic = post_topic
        self.post_qos = post_qos
        self.funcs = funcs
        # self.edge_model_pkg_name = edge_model_pkg_name
        # self.edge_model_func_name = edge_model_func_name
        # self.edge_model_func = self.load_edge_model(self.edge_model_pkg_name, self.edge_model_func_name)
        self.thread_box = []

    def load_edge_model(self, pkgName, funcName):
        module = importlib.import_module(pkgName)
        if hasattr(module, funcName):
            return getattr(module, funcName)
        else:
            raise UnknownArgNum(f"Unable to found the corresponding package {pkgName} or func:{funcName}")

    def pre_threader(self, pre_queue):
        def pre_on_message(client, userdata, msg):
            message = msg.payload.decode('utf-8')
            try:
                log.debug(f"pre_on_message get message from mqtt:{message}")
                pre_queue.put(message, block=False, timeout=TIME_OUT)
            except Exception as e:
                log.debug(f"put msg to the pre_queue Exception:{e}, queue:{pre_queue.qsize()}")

        mqtt_client = MqttClient(self.pre_broker_protocol,
                                 self.pre_broker_host,
                                 self.pre_port,
                                 self.pre_topic,
                                 self.pre_qos,
                                 PacketTypes.SUBSCRIBE,
                                 on_message=pre_on_message)
        try:
            mqtt_client.run_consumer()
        except Exception as e:
            log.debug(f"consume mqtt failed!{e}")
            pass

    def post_threader_t(self):
        print("post_threader_t")
        while True:
            try:
                data = self.pre_queue.get(block=True, timeout=TIME_OUT)
                log.debug(f"post_threader get data:{data}")
            except Exception as e:
                log.debug(f"get from the pre_queue Exception:{e}, queue:{self.pre_queue.qsize()}")
                pass

    def post_threader(self):
        mqtt_client = MqttClient(self.post_broker_protocol,
                                 self.post_broker_host,
                                 self.post_port,
                                 self.post_topic,
                                 self.post_qos,
                                 PacketTypes.PUBLISH)
        while True:
            data = None
            try:
                data = self.post_queue.get(block=True, timeout=TIME_OUT)
                log.debug(f"post_threader get data:{data}")
            except Exception as e:
                log.debug(f"get from the pre_queue Exception:{e}, queue:{self.post_queue.qsize()}")
                pass

            try:
                log.debug(f"post_threader put data:{data}")
                data = json.dumps(data)
                mqtt_client.run_publish(data)
            except Exception as e:
                log.debug(f"publish mqtt failed:{e}")
                pass

    def edge_model_calc(self):
        while True:
            in_data = None
            out_data = None
            try:
                in_data = self.pre_queue.get(block=True, timeout=TIME_OUT)
            except Exception as e:
                log.debug(f"get msg from pre_queue Exception:{e}, queue:{self.pre_queue.qsize()}")

            if in_data is not None:
                to_dict = {}
                try:
                    to_dict = json.loads(in_data)
                except Exception:
                    pass
                # out_data = self.edge_model_func(to_dict, None)
                if self.funcs is not None and len(self.funcs) > 0:
                    for func in self.funcs:
                        if func.device_name == to_dict["deviceInfo"]["deviceName"]:
                            if func.point_name in to_dict["telemetry"] or func.point_name == "":
                                out_data = edge_model_handle(func.model_name, to_dict)
                            else:
                                pass

            if out_data is not None:
                try:
                    self.post_queue.put(out_data, block=True, timeout=TIME_OUT)
                except Exception as e:
                    log.debug(f"put msg to the post_queue Exception:{e}, queue:{self.post_queue.qsize()}")

    def make_run_thead(self):
        reading_thread_name = f"{self.sub_process_name}_read_mqtt"
        reading_thread = threading.Thread(target=self.pre_threader, args=(self.pre_queue,), name=reading_thread_name)
        reading_thread.daemon = True
        self.thread_box.append(reading_thread)

        writing_thread_name = f"{self.sub_process_name}_write_mqtt"
        writing_thread = threading.Thread(target=self.post_threader, name=writing_thread_name)
        writing_thread.daemon = True
        self.thread_box.append(writing_thread)
        # 单进程测试使用
        # edge_model_thread = threading.Thread(target=self.edge_model_calc, args=(0,))
        # edge_model_thread.daemon = True

        reading_thread.start()
        writing_thread.start()

        # 单进程测试使用
        # edge_model_thread.start()

        # 子进程无阻塞,将部分线程运行在子进程的主线程中
        # self.edge_model_calc(0)

        for i in range(MAX_EDGE_NUM):
            edge_model_thread_name = f"{self.sub_process_name}_edge_model_{i}"
            edge_model_thread = threading.Thread(target=self.edge_model_calc, name=edge_model_thread_name)
            edge_model_thread.daemon = True
            self.thread_box.append(edge_model_thread)
            edge_model_thread.start()

    def query_queue_size(self):
        return {"sub_process_name": self.sub_process_name,
                "pre_queue": self.pre_queue.qsize(),
                "post_queue": self.post_queue.qsize()
                }

    def join_thread_from_box(self):
        for t in self.thread_box:
            t.join()
