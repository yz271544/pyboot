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
from pyboot.conf.conf import BaseConfig
from pprint import pprint

from pyboot.conf.settings import PYBOOT_HOME

print("PWD:", os.getcwd())
conf = os.path.join(PYBOOT_HOME, "conf/config.yaml")
df = open(conf, 'r')
config = yaml.load_all(df.read(), Loader=yaml.FullLoader)
print(config)
arrConfList = [BaseConfig]
for content in config:
    arrConf = BaseConfig(**content)
    print(content)
    print(isinstance(content, dict))
    arrConfList.append(arrConf)
df.close()
print("arrConfList:")
pprint(arrConfList)
print(arrConfList[1].name)
print(arrConfList[1].description)
print("arrConf.env:", arrConfList[1].env)
# print("arrConf.env.env_name:", arrConf.env.env_name)
# print("arrConf.env.env_value", arrConf.env.env_value)
print(arrConfList[1].advise_ip)

print()
for e in arrConfList[1].env:
    print(e)


def getBaseConf() -> [BaseConfig]:
    return arrConfList
