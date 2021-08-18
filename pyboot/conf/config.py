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


class EdgeModelConfig(marshmallow.Model):
    instance = marshmallow.fields.Int()
    pre_broker = marshmallow.fields.Str()
    pre_port = marshmallow.fields.Int()
    pre_topic = marshmallow.fields.Str()
    pre_qos = marshmallow.fields.Int()
    edge_mode = marshmallow.fields.Str()
    post_broker = marshmallow.fields.Str()
    post_port = marshmallow.fields.Int()
    post_topic = marshmallow.fields.Str()
    post_qos = marshmallow.fields.Int()

    def edge_mode_package(self):
        """
        :return: (packageName, funcName)
        """
        edgemode = self.edge_mode
        slist = str(edgemode).split('.')
        return '.'.join(slist[:-1]), slist[-1]


class BaseConfig(marshmallow.Model):
    app_name = marshmallow.fields.Str()
    description = marshmallow.fields.Str()
    edge = marshmallow.fields.List(marshmallow.NestedModel(EdgeModelConfig))

    def __repr__(self):
        return "%s(name=%r, description=%r, edge=%r)" % (self.__class__.name, self.name, self.description, json.dumps(self.edge))

