#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: ChkSum.py
@author: etl
@time: Created on 11/25/21 1:47 PM
@env: Python @desc:
@ref: @blog:
"""
import os
import hashlib
import base64


def GetFileMd5Byte(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.digest()


def GetFileMd5Str(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def GetBase64Md5Byte(md5_value):
    base64_md5 = base64.encodebytes(md5_value)
    # sbm = bytes.decode(base64_md5)
    sbm = str(base64_md5, encoding="utf-8")
    sbm = ''.join(sbm[:-1].split())
    return sbm

