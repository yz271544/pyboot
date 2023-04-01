#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: processor_starter.py
@author: etl
@time: Created on 8/18/21 6:27 PM
@env: Python @desc:
@ref: @blog:
"""
import os
import sys
from pyboot.conf import BaseConfig
from pyboot.conf.base_conf_starter import Props
from pyboot.conf.settings import DOWNLOAD_MODEL, MODEL_PATH, PYBOOT_HOME, MODEL_REF_PREFIX
from pyboot.core.MqttProcessor import MqttProcessor
from pyboot.logger import log
from pyboot.starter import BaseStarter
from pyboot.starter_context import StarterContext
from pyboot.utils.model.model import download_by_funcs


def _prepare_pickle_models_path():
    """
    # Pickle depends on the module path. So, should make sure that the module index.py is in sys.path.
    """
    dir_path_root_slice = (str(PYBOOT_HOME).split("/"))[:-1]
    DIR_PYBOOT = '/'.join(dir_path_root_slice)
    models_dir_name = DIR_PYBOOT + "/" + MODEL_REF_PREFIX
    for path, currentDirectory, files in os.walk(models_dir_name):
        for f in files:
            if ".model" in f:
                pickle_file_full_path = "%s/%s" % (path, f)
                model_dir_name = os.path.dirname(pickle_file_full_path)
                if model_dir_name not in sys.path:
                    log.info("add model dir from %s" % model_dir_name)
                    sys.path.append(model_dir_name)


class ProcessorStarter(BaseStarter):
    def __init__(self):
        self.props = None
        self.processor = None

    def Init(self, starter_context: StarterContext):
        log.info("ProcessorStarter Init start")
        props = Props()
        print(props.__class__.__name__) # BaseConfig
        self.props = props
        # if DOWNLOAD_MODEL:
        #     download_by_funcs(self.props.funcs)
        log.info("初始化配置")
        log.info("ProcessorStarter Init end")
        return

    def Setup(self, starter_context):
        log.info("ProcessorStarter Setup Begin...")
        if DOWNLOAD_MODEL:
            download_by_funcs(self.props.funcs)
        if self.props is not None and len(self.props.edge) > 0:
            self.processor = MqttProcessor(self.props.edge, self.props.funcs)
        _prepare_pickle_models_path()
        log.info("ProcessorStarter Setup END...")
        return

    def Start(self, starter_context):
        log.info("ProcessorStarter Start Begin...")
        if self.processor is not None:
            self.processor.process()
        log.info("ProcessorStarter Start END...")
        return

    def Stop(self, starter_context):
        log.info("ProcessorStarter Stop Begin...")
        self.processor.teardown()
        log.info("ProcessorStarter Stop END...")
