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
import re
import platform
import urllib3
from pyboot.conf import EdgeFuncConfig
from urllib.parse import urlparse
from pyboot.logger import log
from pyboot.conf.settings import MODEL_PATH, CHECK_SIZE
from pyboot.utils.common.compress_utils import un_zip, un_gz, un_tar
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
            try:
                log.info("try download model %s" % download_target_file)
                # un_zip(download_target_file, uncompress_model_dir)
                _uncompress_according_to_ext_name(download_target_file, uncompress_model_dir)
            except Exception as e:
                log.error(f"unzip file {download_target_file} failed: {e}", stack_info=True)
            try:
                os.remove(download_target_file)
            except Exception as e:
                log.error(f"remove file {download_target_file} failed", stack_info=True)


def download(http, **kwargs):
    func = kwargs['func']
    current_system_arch = recognize_machine_arch()
    model_address = ""
    if current_system_arch in ["amd64"]:
        model_address = func.model_amd64_address
    elif current_system_arch in ["arm64"]:
        model_address = func.model_arm64_address
    else:
        log.fatal("Unsupport system architecture")
        exit("Unsupport system architecture")

    model_compress_file_name = extract_filename_from_url(model_address)

    download_target_file = os.path.join(MODEL_PATH, model_compress_file_name)
    log.info(download_target_file)

    if os.path.exists(download_target_file):
        log.debug("%s file is exists" % download_target_file)
    else:
        r = None
        try:
            log.info(f"try download model: {model_address}")
            r = http.request(
                'GET',
                model_address,
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
            log.error(f"download model:{model_address} failed!", stack_info=True)
        # finally:
        #     r.release_conn()
    return download_target_file


def recognize_machine_arch():
    sys_arch = platform.machine()
    if sys_arch in ["i386", "x86", "x32"]:
        return "amd"
    elif sys_arch in ["amd64", "AMD64", "x86_64", "x64"]:
        return "amd64"
    elif sys_arch in ["arm", "arm4", "arm5", "arm6", "arm7"]:
        return "arm"
    elif sys_arch in ["arm64", "arm8", "aarch64"]:
        return "arm64"
    else:
        return "unknown"


def extract_filename_from_url(url):
    parse_result = urlparse(url)
    return os.path.basename(parse_result.path)


def _uncompress_according_to_ext_name(file_full_name, uncompress_target_dir):
    re_regex = r".*.tar.gz$"
    file_base_name = os.path.basename(file_full_name)
    file_name_tuple = os.path.splitext(file_base_name)
    match = re.match(re_regex, file_full_name)
    if match:
        log.info("uncompres tar.gz %s to %s" % (file_full_name, uncompress_target_dir))
        un_gz(file_full_name, uncompress_target_dir)
        un_gz_file_name = file_name_tuple[0]
        un_gz_file_full_name = os.path.join(uncompress_target_dir, un_gz_file_name)
        un_tar(un_gz_file_full_name, uncompress_target_dir)
        os.remove(un_gz_file_full_name)
    else:
        ext_name = file_name_tuple[1]
        if ext_name == ".gz":
            log.info("un_gz %s to %s" % (file_full_name, uncompress_target_dir))
            un_gz(file_full_name, uncompress_target_dir)
        elif ext_name == ".tar":
            log.info("un_tar %s to %s" % (file_full_name, uncompress_target_dir))
            un_tar(file_full_name, uncompress_target_dir)
        elif ext_name == ".zip":
            log.info("un_zip %s to %s" % (file_full_name, uncompress_target_dir))
            un_zip(file_full_name, uncompress_target_dir)
