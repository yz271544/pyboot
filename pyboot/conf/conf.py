#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: conf.py
@author: etl
@time: Created on 8/13/21 2:00 PM
@env: Python @desc:
@ref: @blog:
"""

import marshmallow_objects as marshmallow


class BaseConfig(marshmallow.Model):
    name = marshmallow.fields.Str()
    description = marshmallow.fields.Str()
    env = marshmallow.fields.List(marshmallow.fields.Dict())
    advise_ip = marshmallow.fields.List(marshmallow.fields.Str)

    def __repr__(self):
        return "%s(name=%r, description=%r, env=%r, advise_ip=%r)" % (self.__class__.name, self.name, self.description, self.env, self.advise_ip)

