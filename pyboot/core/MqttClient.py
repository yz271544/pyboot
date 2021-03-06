#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: MqttClient.py
@author: etl
@time: Created on 8/18/21 10:40 AM
@env: Python @desc:
@ref: @blog:
"""
import time
import random
from paho.mqtt import client as mqtt_client
from paho.mqtt.packettypes import PacketTypes
from pyboot.conf.settings import MAX_PUBLISH_RETRY

from pyboot.logger import log
from pyboot.utils.error.Errors import UnknownArgNum, SystemUnknownError


class MqttClient:

    def __init__(self, protocol: str, host: str, port: int, topic: str, qos: int,
                 packet_type: PacketTypes, on_message=None):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.topic = topic
        self.qos = qos
        self.client_id = f"python-mqtt-{random.randint(0, 100)}"
        self.packet_type = packet_type
        self.on_message = on_message
        self.client = self.connect_mqtt(self.topic, self.qos)

    def connect_mqtt(self, topic, qos):
        def on_log(client, userdata, level, buf):
            log.debug(buf)

        def on_connect_subscribe(client, userdata, flags, rc):
            # print("flags: ", flags)
            if rc == 0:
                log.debug("Connected to MQTT Broker!")
                client.subscribe(topic, qos)
            else:
                log.error(f"Failed to connect, return code {rc}", stack_info=True)

        def on_connect_publish(client, userdata, flags, rc):
            if rc == 0:
                log.debug("Connected to MQTT Broker!")
            else:
                log.error(f"Failed to connect, return code {rc}", stack_info=True)

        def on_disconnect(client, userdata, flags, rc=0):
            log.error(f"Disconnected result code:{str(rc)}", stack_info=True)

        # def on_message(client, userdata, msg):
        #     print(f"Received {msg.payload.decode('utf-8')} from {msg.topic} topic")

        # Set Connecting Client ID
        client = mqtt_client.Client(self.client_id, transport=self.protocol)
        if self.packet_type == PacketTypes.SUBSCRIBE:
            client.on_connect = on_connect_subscribe
        elif self.packet_type == PacketTypes.PUBLISH:
            client.on_connect = on_connect_publish
        else:
            raise UnknownArgNum("The packet_type must be in the [PacketTypes.SUBSCRIBE, PacketTypes.PUBLISH]")
        client.on_disconnect = on_disconnect
        if self.on_message is not None:
            client.on_message = self.on_message
        client.on_log = on_log
        while True:
            try:
                client.connect(self.host, self.port)
                break
            except ConnectionRefusedError as e:
                log.error(f"connection mqtt {self.host}:{self.port} refuse error:{e}", stack_info=True)
                time.sleep(5)
                continue
        # client.loop_start()
        return client

    def run_consumer(self):
        # client = self.connect_mqtt(self.topic)
        try:
            self.client.loop_forever()
        except Exception as e:
            log.error(f"loop_forever error:{e}", stack_info=True)

    def run_publish(self, message, retrys=0):
        self.client.loop_start()
        if retrys == MAX_PUBLISH_RETRY:
            return
        result = self.client.publish(self.topic, message, self.qos)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            log.debug(f"Send {message} to topic {self.topic}")
            return
        else:
            log.error(f"Failed to send message to topic {self.topic}", stack_info=True)
            retrys += 1
            self.run_publish(message, retrys)

    # def publish(self, client, msg):
    #     while True:
    #         result = client.publish(self.topic, msg, 0)
    #         # result: [0, 1]
    #         status = result[0]
    #         if status == 0:
    #             print(f"Send {msg} to topic {self.topic}")
    #         else:
    #             print(f"Failed to send message to topic {self.topic}")
