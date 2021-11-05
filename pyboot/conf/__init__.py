#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: __init__.py.py
@author: etl
@time: Created on 8/13/21 9:37 AM
@env: Python @desc:
@ref: @blog:
"""
import os
import yaml
from pyboot.conf.config import BaseConfig, MqttSchema, RuleSchema, EdgeModelConfig, parse_host

from pyboot.conf.settings import PYBOOT_HOME
from pyboot.utils.common.SnowflakeId import IdWorker

global_mqtt_dict = {}
global_rules = []
id_worker = IdWorker.get_instance()


def load_from_config():
    new_conf = os.path.join(PYBOOT_HOME, "conf/config.yaml")
    with open(new_conf, 'r') as cf:
        cnf = yaml.load(cf.read(), Loader=yaml.FullLoader)
        mqtt_schema = MqttSchema(many=True)
        rule_schema = RuleSchema(many=True)
        mqtts = mqtt_schema.dump(cnf['mqtts'])
        for mqtt in mqtts:
            global_mqtt_dict[mqtt['name']] = mqtt

        rules = rule_schema.dump(cnf['rules'])
        for rule in rules:
            global_rules.append(rule)


def get_mqtt_conf() -> dict:
    """
    parse the mqtts dict from config file
    :return:
    """
    return global_mqtt_dict


def get_rule_conf() -> [RuleSchema]:
    """
    parse and get the rules from config file
    :return:
    """
    return global_rules


def get_base_conf() -> BaseConfig:
    mqtt_dict = get_mqtt_conf()
    rules = get_rule_conf()

    edges = [EdgeModelConfig]
    for rule in rules:
        sub_info = rule['sub']
        sub_name = sub_info['name']
        mqtt_sub_info = mqtt_dict[sub_name]
        (sub_protocol, sub_host, sub_port) = parse_host(mqtt_sub_info['brokers'])

        pub_info = rule['pub']
        pub_name = pub_info['name']
        mqtt_pub_info = mqtt_dict[pub_name]
        (pub_protocol, pub_host, pub_port) = parse_host(mqtt_pub_info['brokers'])

        edge_model_config = EdgeModelConfig(rule['name'],
                                            pre_broker_protocol=sub_protocol,
                                            pre_broker_host=sub_host,
                                            pre_broker_port=int(sub_port),
                                            pre_qos=int(mqtt_sub_info['qos']),
                                            pre_retain=mqtt_sub_info['retain'],
                                            pre_topic=sub_info['topic'],
                                            edge_mode=rule['func'],
                                            post_broker_protocol=pub_protocol,
                                            post_broker_host=pub_host,
                                            post_broker_port=pub_port,
                                            post_qos=int(mqtt_pub_info['qos']),
                                            post_retain=mqtt_pub_info['retain'],
                                            post_topic=pub_info['topic'],
                                            )
        edges.append(edge_model_config)

    return BaseConfig("test", "test", edges)


def get_id_worker() -> IdWorker:
    return id_worker


if not bool(global_mqtt_dict) and not bool(global_rules):
    load_from_config()
