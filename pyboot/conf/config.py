#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: config.py
@author: etl
@time: Created on 8/13/21 2:00 PM
@env: Python @desc:
@ref: @blog:
"""
import json
import marshmallow_objects as marshmallow


class EdgeModelConfig(json.JSONEncoder):

    def __init__(self, name, instance=1, **kwargs):
        super().__init__()
        self.name = name
        self.instance = instance
        self.pre_broker_protocol = kwargs['pre_broker_protocol']
        self.pre_broker_host = kwargs['pre_broker_host']
        self.pre_broker_port = kwargs['pre_broker_port']
        self.pre_topic = kwargs['pre_topic']
        self.pre_qos = kwargs['pre_qos']
        self.pre_retain = kwargs['pre_retain']
        self.post_broker_protocol = kwargs['post_broker_protocol']
        self.post_broker_host = kwargs['post_broker_host']
        self.post_broker_port = kwargs['post_broker_port']
        self.post_topic = kwargs['post_topic']
        self.post_qos = kwargs['post_qos']
        self.post_retain = kwargs['post_retain']

    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)

    # def edge_mode_package(self):
    #     """
    #     :return: (packageName, funcName)
    #     """
    #     edgemode = self.edge_mode
    #     slist = str(edgemode).split('.')
    #     return '.'.join(slist[:-1]), slist[-1]

    def __repr__(self):
        return "%s(name=%r, instance=%r, " \
               "pre_broker_protocol=%r, pre_broker_host=%r, pre_broker_port=%r, " \
               "pre_topic=%r, pre_qos=%r, pre_retain=%r, " \
               "post_broker_protocol=%r, post_broker_host=%r, post_broker_port=%r, " \
               "post_topic=%r, post_qos=%r, post_retain=%r)" % (
                   self.__class__.__name__, self.name, self.instance,
                   self.pre_broker_protocol, self.pre_broker_host, self.pre_broker_port,
                   self.pre_topic, self.pre_qos, self.pre_retain,
                   self.post_broker_protocol, self.post_broker_host, self.post_broker_port,
                   self.post_topic, self.post_qos, self.post_retain)


class EdgeFuncConfig(json.JSONEncoder):

    def __init__(self, **kwargs):
        super().__init__()
        self.model_address = kwargs['modelAddress'] if 'modelAddress' in kwargs else ""
        self.model_md5 = kwargs['modelMd5'] if 'modelMd5' in kwargs else ""
        self.model_name = kwargs['modelName'] if 'modelName' in kwargs else ""
        self.devices = kwargs['devices'] if 'devices' in kwargs else []

    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)

    def __repr__(self):
        return "%s(model_address=%r, model_md5=%r, model_name=%r, " \
               "devices=%r)" % (
                   self.__class__.__name__, self.model_address, self.model_md5, self.model_name, self.devices)


class BaseConfig(json.JSONEncoder):

    def __init__(self, edge: [EdgeModelConfig], funcs: [EdgeFuncConfig]):
        super().__init__()
        self.edge = edge
        self.funcs = funcs

    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)

    def __repr__(self):
        return "%s(edge=%r, funcs=%r)" % (
            self.__class__.__name__, json.dumps(self.funcs), json.dumps(self.edge))


class MqttSchema(marshmallow.Schema):
    name = marshmallow.fields.Str()
    broker = marshmallow.fields.Str()
    qos = marshmallow.fields.Int()
    retain = marshmallow.fields.Bool()

    @marshmallow.post_load
    def make_mqtt(self, data, **kwargs):
        return MqttSchema(**data)

    def __repr__(self):
        return "%s(name=%r, broker=%r, retain=%r)" % (
            self.__class__.name, self.name, self.broker, json.dumps(self.retain))


class RuleSubSchema(marshmallow.Schema):
    name = marshmallow.fields.Str()
    clientId = marshmallow.fields.Str()
    topic = marshmallow.fields.Str()

    @marshmallow.post_load
    def make_rule_sub(self, data, **kwargs):
        return RuleSubSchema(**data)

    def __repr__(self):
        return "%s(name=%r, clientId=%r, topic=%r)" % (
            self.__class__.name, self.name, self.clientId, json.dumps(self.topic))


class RulePubSchema(marshmallow.Schema):
    name = marshmallow.fields.Str()
    clientId = marshmallow.fields.Str()
    timeout = marshmallow.fields.Str()
    topic = marshmallow.fields.Str()

    @marshmallow.post_load
    def make_rule_pub(self, data, **kwargs):
        return RulePubSchema(**data)

    def __repr__(self):
        return "%s(name=%r, clientId=%r, timeout=%r, topic=%r)" % (
            self.__class__.name, self.name, self.clientId, self.timeout, self.topic)


class RuleSchema(marshmallow.Schema):
    name = marshmallow.fields.Str()
    sub = marshmallow.fields.Nested(RuleSubSchema)
    pub = marshmallow.fields.Nested(RulePubSchema)

    @marshmallow.post_load
    def make_rule(self, data, **kwargs):
        return RuleSchema(**data)

    def __repr__(self):
        return "%s(name=%r, sub=%r, pub=%r)" % (
            self.__class__.__name__, self.name, json.dumps(self.sub), json.dumps(self.pub))


class DeviceAttrSchema(marshmallow.Schema):
    attrName = marshmallow.fields.Str()
    attrValue = marshmallow.fields.Str()
    attrExpression = marshmallow.fields.Str()

    @marshmallow.post_load
    def make_rule(self, data, **kwargs):
        return DeviceAttrSchema(**data)

    def __repr__(self):
        return "%s(attrName=%r, attrValue=%r, attrExpression=%r)" % (
            self.__class__.__name__, self.attrName, self.attrValue, self.attrExpresion
        )


class DeviceSchema(marshmallow.Schema):
    deviceName = marshmallow.fields.Str()
    deviceAttr = marshmallow.fields.Nested(DeviceAttrSchema, many=True)

    @marshmallow.post_load
    def make_rule(self, data, **kwargs):
        return DeviceSchema(**data)

    def __repr__(self):
        return "%s(device=%r, deviceName=%r, deviceAttr=%r)" % (
            self.__class__.__name__, self.deviceName, self.deviceAttr
        )


class FuncSchema(marshmallow.Schema):
    modelAddress = marshmallow.fields.Str()
    modelMd5 = marshmallow.fields.Str()
    modelName = marshmallow.fields.Str()
    devices = marshmallow.fields.Nested(DeviceSchema, many=True)

    @marshmallow.post_load
    def make_rule(self, data, **kwargs):
        return FuncSchema(**data)

    def __repr__(self):
        return "%s(modelAddress=%r, modelMd5=%r, modelName=%r, devices=%r)" % (
            self.__class__.__name__, self.modelAddress, self.modelMd5,
            self.modelName, self.devices)


def parse_host(broker: str) -> (str, str, str):
    """
    parse the broker to protocol host port
    :param broker:
    :return: protocol host port
    """
    (protocol, host_port) = broker.split("://")
    (host, port) = host_port.split(":")
    return protocol, host, port
