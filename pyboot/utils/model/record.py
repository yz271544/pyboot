#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: record.py
@author: etl
@time: Created on 11/25/21 2:39 PM
@env: Python @desc:
@ref: @blog:
"""

from pyboot.conf.settings import MODEL_RECORD


class ModelRecord(object):
    """A class for the model record and map file
       use ### split the fields
       field0: model_name
       field1: md5
    """
    def __init__(self):
        self.model_record_dict = {}
        self.record_file = open(MODEL_RECORD, 'r+')
        lines = self.record_file.readlines()
        for line in lines:
            record_tup = line.split("###")
            md5_value = record_tup[1]
            md5_value = ''.join(md5_value[:-1].split())
            self.model_record_dict[record_tup[0]] = md5_value

    def __del__(self):
        self.record_file.close()

    def __add(self, func):
        model_name = func.model_name
        model_md5 = func.model_md5
        self.model_record_dict[model_name] = model_md5
        self.record_file.write("###".join([model_name, model_md5])+"\n")

    def __get(self, func):
        model_name = func.model_name
        model_md5 = func.model_md5
        if model_name in self.model_record_dict:
            if model_md5 == self.model_record_dict[model_name]:
                return self.model_record_dict[model_name]
            return None
        else:
            return None

    def truncate(self):
        self.record_file.truncate(0)
        self.model_record_dict.clear()

    def determine(self, func):
        """
        Determine if func exists
        :param func:
        :return: bool
        True: Already exists
        False: Not yet exist
        """
        searched = self.__get(func)
        if searched is None:
            self.__add(func)
            return False
        else:
            return True
