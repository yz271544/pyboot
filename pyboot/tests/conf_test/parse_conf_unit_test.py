#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: base_test.py
@author: etl
@time: Created on 8/13/21 12:33 PM
@env: Python @desc:
@ref: @blog:
"""

import os
import unittest
import urllib3
from urllib.parse import urlparse
from pyboot.conf import load_from_config, global_mqtt_dict, global_rules, global_funcs, PYBOOT_HOME
from pyboot.conf.settings import MODEL_PATH
from pyboot.utils.common.ChkSum import GetFileMd5Byte, GetBase64Md5Byte
from pyboot.utils.model.model import extract_filename_from_url


class ParseConfUnitTest(unittest.TestCase):

    def test_max_int(self):
        load_from_config(config_file_path="/lyndon/iProject/pypath/pyboot/pyboot/conf/config.yaml")
        print(global_mqtt_dict)
        print(global_rules)
        print(global_funcs)

    def test_convert_bool(self):
        offon = "True"
        print(bool(offon))

    def test_extract_filename(self):
        url = "http://10.200.60.18:9000/group1/M00/01/0D/Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip"
        a = urlparse(url)
        print(a.path)  # Output: /group1/M00/01/0D/Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip
        print(os.path.basename(a.path))  # Output: Ch1hQF_5ZN2AeOGUAAAejBbqmSQ670.zip

    def test_echo_PYBOOT_HOME(self):
        print(PYBOOT_HOME)
        print(MODEL_PATH)

    def test_download(self):
        chunk_size = 2048
        http = urllib3.PoolManager()
        url = "http://10.200.60.18:9000/group1/M00/49/04/Csg8EmGdnIyAVJdVAAHaY0adxNc829.zip"
        model_compress_file_name = extract_filename_from_url(url)

        download_target_file = os.path.join(MODEL_PATH, model_compress_file_name)
        print(download_target_file)

        if os.path.exists(download_target_file):
            print("%s file is exists" % download_target_file)
            os.remove(download_target_file)
            print("remove file %s" % download_target_file)
        else:
            r = http.request(
                'GET',
                url,
                preload_content=False
            )

            with open(download_target_file, 'wb') as out:
                while True:
                    data = r.read(chunk_size)
                    if not data:
                        break
                    out.write(data)

            print(r.status)
            print(r.headers)
            r.release_conn()

    def test_file_base64_md5(self):
        # target_file = "/lyndon/iProject/pypath/pyboot/pyboot/modules/gridsum/science/Csg8EmGdnIyAVJdVAAHaY0adxNc829.zip"
        target_file = "/home/etl/cps/Ch1hQGGkxnSAIiFrAAO8COz2yGE652.zip"
        md5_value = GetFileMd5Byte(target_file)
        print('md5_value:', md5_value)
        # base64_md5 = base64.encodebytes(md5_value)
        #
        # print(base64_md5)
        # print(type(base64_md5))
        # # sbm = bytes.decode(base64_md5)
        # sbm = str(base64_md5, encoding="utf-8")
        # sbm = ''.join(sbm[:-1].split())
        sbm = GetBase64Md5Byte(md5_value)
        print('sbm:', sbm)
        print(type(sbm))

    #
    def test_file_base64_md5_2(self):
        target_file = "/home/etl/cps/Ch1hQGGkxnSAIiFrAAO8COz2yGE652.zip"
        md5_value = GetFileMd5Byte(target_file)
        print("md5_value:", md5_value)
        sbm = GetBase64Md5Byte(md5_value)
        print('sbm:', sbm)
        print(type(sbm))

