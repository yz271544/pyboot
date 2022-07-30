#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: test_conf_parse.py
@author: etl
@time: Created on 11/4/21 3:38 PM
@env: Python @desc: pytest -s -m "base" pyboot/tests/conf_test/test_conf_parse.py
@ref: @blog:
"""
import json
import os
import pytest
import yaml

from pyboot.conf import PYBOOT_HOME, get_mqtt_conf, get_base_conf

# pytest -s -m "base" pyboot/tests/conf_test/test_conf_parse.py::test_load_from_yaml
from pyboot.conf.config import MqttSchema, RuleSchema, parse_host, BaseConfig


@pytest.mark.base
def test_load_from_yaml():
    conf = os.path.join(PYBOOT_HOME, "conf/config.yaml")
    df = open(conf, 'r')
    config = yaml.load(df.read(), Loader=yaml.FullLoader)
    print(config)
    print(type(config))

    print(config['mqtts'])

    print("-----------------------------------------------------")
    cnf = config['mqtts']

    print(type(cnf))

    mqtt_schema = MqttSchema(many=True)

    mqtts = mqtt_schema.dump(cnf)

    print(mqtts)

    for e in mqtts:
        print(e)


# pytest -s -m "base" pyboot/tests/conf_test/test_conf_parse.py::test_load_rules
@pytest.mark.base
def test_load_rules():
    conf = os.path.join(PYBOOT_HOME, "conf/config.yaml")
    df = open(conf, 'r')
    config = yaml.load(df.read(), Loader=yaml.FullLoader)
    print(config)
    print(type(config))

    print(config['rules'])

    print("-----------------------------------------------------")
    cnf = config['rules']

    print(type(cnf))

    rule_schema = RuleSchema(many=True)

    rules = rule_schema.dump(cnf)

    print(rules)

    for e in rules:
        print(e)


@pytest.mark.base
def test_loads_rules():
    base_config = get_base_conf()
    # print(base_config)
    print(json.dumps(base_config, cls=BaseConfig, indent=4))


@pytest.mark.base
def test_parse_host():
    broker = "tcp://192.168.241.1:1883"
    (protocol, host, port) = parse_host(broker)
    print(protocol, host, port)


@pytest.mark.base
def test_mqtt_conf():
    mqtt_dict = get_mqtt_conf()
    print(mqtt_dict)
