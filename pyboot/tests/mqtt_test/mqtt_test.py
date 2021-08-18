#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: mqtt_test.py
@author: etl
@time: Created on 8/18/21 11:10 AM
@env: Python @desc:
@ref: @blog:
"""

import pytest
from paho.mqtt.packettypes import PacketTypes

@pytest.mark.base
def test_properties():
    print(PacketTypes.SUBSCRIBE)
    print(PacketTypes.PUBLISH)
    print(PacketTypes.Names[PacketTypes.SUBSCRIBE])
    print(PacketTypes.Names[PacketTypes.PUBLISH])


