#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: model.py
@author: etl
@time: Created on 11/24/21 8:20 PM
@env: Python @desc:
@ref: @blog:
"""
import os
import urllib3
from pyboot.conf import EdgeFuncConfig
from urllib.parse import urlparse
from pyboot.logger import log
from pyboot.conf.settings import MODEL_PATH, CHECK_SIZE
from pyboot.utils.common.compress_utils import un_zip
from pyboot.utils.model.record import ModelRecord


def download_by_funcs(funcs: [EdgeFuncConfig]):
    """
    download science model
    record the model file by md5
    :param funcs:
    :return:
    """
    http = urllib3.PoolManager()
    model_record = ModelRecord()
    for func in funcs:
        is_exists = model_record.determine(func)
        if is_exists:
            continue
        else:
            download_target_file = download(http, func=func)
            uncompress_model_dir = os.path.join(MODEL_PATH, func.model_name)
            un_zip(download_target_file, uncompress_model_dir)
            os.remove(download_target_file)


def download(http, **kwargs):
    func = kwargs['func']
    model_compress_file_name = extract_filename_from_url(func.model_address)

    download_target_file = os.path.join(MODEL_PATH, model_compress_file_name)
    log.info(download_target_file)

    if os.path.exists(download_target_file):
        log.debug("%s file is exists" % download_target_file)
    else:
        r = None
        try:
            log.info(f"try download model: {func.model_address}")
            r = http.request(
                'GET',
                func.model_address,
                preload_content=False
            )

            with open(download_target_file, 'wb') as out:
                while True:
                    data = r.read(CHECK_SIZE)
                    if not data:
                        break
                    out.write(data)

            log.info("download %s, status: %r, header: %r" % (download_target_file, r.status, r.headers))
            r.release_conn()
        except Exception as e:
            log.error(f"download model:{func.model_address} failed!")
        # finally:
        #     r.release_conn()
    return download_target_file


def extract_filename_from_url(url):
    parse_result = urlparse(url)
    return os.path.basename(parse_result.path)


