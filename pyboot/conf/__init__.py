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
import sys
from optparse import OptionParser, OptionGroup
from pyboot.conf.config import BaseConfig, MqttSchema, RuleSchema, EdgeModelConfig, parse_host, FuncSchema, \
    EdgeFuncConfig

from pyboot.conf.settings import PYBOOT_HOME
from pyboot.utils.common.SnowflakeId import IdWorker

global_mqtt_dict = {}
global_rules = []
global_funcs = []
id_worker = IdWorker.get_instance()


def get_option_parser():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    option_group = OptionGroup(parser, "set the prog config file for pyboot.")
    option_group.add_option("-c", "--config", metavar="<goboot.yaml path>",
                            dest="config",
                            action="store",
                            default="",
                            type="string",
                            help="set the prog config file.")

    parser.add_option_group(option_group)
    return parser


def load_from_config(option=None, config_file_path=""):
    if option != None:
        config_file_path = option.config
        if config_file_path == "":
            config_file_path = os.path.join(PYBOOT_HOME, "conf/config.yaml")
    with open(config_file_path, 'r') as cf:
        cnf = yaml.load(cf.read(), Loader=yaml.FullLoader)
        mqtt_schema = MqttSchema(many=True)
        rule_schema = RuleSchema(many=True)
        func_schema = FuncSchema(many=True)
        mqtts = mqtt_schema.dump(cnf['mqtts'])
        for mqtt in mqtts:
            if "qos" not in mqtt:
                mqtt["qos"] = 0
            if "retain" not in mqtt:
                mqtt["retain"] = False
            global_mqtt_dict[mqtt['name']] = mqtt

        rules = rule_schema.dump(cnf['rules'])
        for rule in rules:
            if "timeout" not in rule["pub"]:
                rule["pub"]["timeout"] = "10s"
            global_rules.append(rule)

        funcs = func_schema.dump(cnf['funcs'])
        for func in funcs:
            global_funcs.append(func)


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


def get_func_conf() -> [FuncSchema]:
    """
    parse and get the funcs from config file
    :return:
    """
    return global_funcs


def get_base_conf() -> BaseConfig:
    mqtt_dict = get_mqtt_conf()
    rules = get_rule_conf()
    funcs = get_func_conf()

    edges = []
    for rule in rules:
        sub_info = rule['sub']
        sub_name = sub_info['name']
        mqtt_sub_info = mqtt_dict[sub_name]
        (sub_protocol, sub_host, sub_port) = parse_host(mqtt_sub_info['broker'])

        pub_info = rule['pub']
        pub_name = pub_info['name']
        mqtt_pub_info = mqtt_dict[pub_name]
        (pub_protocol, pub_host, pub_port) = parse_host(mqtt_pub_info['broker'])

        edge_model_config = EdgeModelConfig(rule['sub'],
                                            pre_broker_protocol=sub_protocol,
                                            pre_broker_host=sub_host,
                                            pre_broker_port=int(sub_port),
                                            pre_qos=int(mqtt_sub_info['qos']),
                                            pre_retain=mqtt_sub_info['retain'],
                                            pre_topic=sub_info['topic'],
                                            post_broker_protocol=pub_protocol,
                                            post_broker_host=pub_host,
                                            post_broker_port=int(pub_port),
                                            post_qos=int(mqtt_pub_info['qos']),
                                            post_retain=mqtt_pub_info['retain'],
                                            post_topic=pub_info['topic'],
                                            )
        edges.append(edge_model_config)

    edge_funcs = []
    for func in funcs:
        edge_func_config = EdgeFuncConfig(**func)
        edge_funcs.append(edge_func_config)

    return BaseConfig(edges, edge_funcs)


def get_id_worker() -> IdWorker:
    return id_worker


# args = ["--config", "/etc/pyboot/config.yaml", "abc", "123"]
parser = get_option_parser()
print("ARGV LEN:", len(sys.argv))
if len(sys.argv) > 0:
    options, args = parser.parse_args(sys.argv[1:])
    if not bool(global_mqtt_dict) and not bool(global_rules) and not bool(global_funcs):
        load_from_config(options)
