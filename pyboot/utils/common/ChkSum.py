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


def get_md5_from_small_file(file_path):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path,'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5


def get_md5_from_big_file(file_path):
    f = open(file_path,'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
    return md5
