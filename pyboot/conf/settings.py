#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@file: settings.py
@author: lyndon
@time: Created on 2021-01-15 10:51
@env: Python
@desc:
@ref:
@blog:
"""

import os
import sys


# print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))
# 调试模式是否开启
DEBUG = False

SQLALCHEMY_TRACK_MODIFICATIONS = False

# SQLALCHEMY_NATIVE_UNICODE = True

SECRET_KEY = 'huzhengyang@bonc.com'

# SQLALCHEMY_POOL_TIMEOUT = 60

SQLALCHEMY_ENGINE_OPTIONS = {}

SQLALCHEMY_ENGINE_OPTIONS['pool_timeout'] = 60
# SQLALCHEMY_ENGINE_OPTIONS['supports_unicode_statements'] = True
# SQLALCHEMY_ENGINE_OPTIONS['supports_unicode_binds'] = True

REHEARSAL_START_STATUS = 6
REHEARSAL_SUCCESS_STATUS = 7
REHEARSAL_ERROR_STATUS = 13

SUB_PROCESS_BLOCK = True
SUB_PROCESS_TIMEOUT = 120

SUB_THREAD_BLOCK = True
SUB_THREAD_TIMEOUT = 120

try:
    PYBOOT_HOME = os.environ["PYBOOT_HOME"]
except Exception as e:
    curPath = os.path.abspath(os.path.dirname(__file__))
    # print("settings curPath:", curPath)
    rootPath = os.path.split(curPath)[0]
    # print("settings rootPath:", rootPath)
    PYBOOT_HOME = rootPath
    sys.path.append(rootPath)
    # print("settings sys.path:", sys.path)
    # PYBOOT_HOME = os.getcwd()

sys.path.append(os.path.dirname(os.getcwd()))

try:
    PROFILE = os.environ["PYBOOT_PROFILE"]
except Exception as e:
    PROFILE = 'dev'

if PROFILE == 'dev':
    SERV_PORT = 5888
    JDBC_MYSQL_DRIVER = "mysql"
    MYSQL_DRIVER = "pymysql"
    MYSQL_USERNAME = "foxmind"
    MYSQL_PASSWORD = "Foxmind0827!"
    MYSQL_SERVER = "42.193.113.130:3306"
    DB_NAME = "foxmind"
    DB_CHARSET = "utf8"
    SQLALCHEMY_DATABASE_URI = "{JDBC_MYSQL_DRIVER}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{DB_NAME}?charset={DB_CHARSET}".format(
        JDBC_MYSQL_DRIVER=JDBC_MYSQL_DRIVER, MYSQL_DRIVER=MYSQL_DRIVER, MYSQL_USERNAME=MYSQL_USERNAME,
        MYSQL_PASSWORD=MYSQL_PASSWORD, MYSQL_SERVER=MYSQL_SERVER, DB_NAME=DB_NAME, DB_CHARSET=DB_CHARSET)
    SQLALCHEMY_ECHO = True  # 打印原始sql

elif PROFILE == 'test':
    SERV_PORT = 5888
    JDBC_MYSQL_DRIVER = "mysql"
    MYSQL_DRIVER = "pymysql"
    MYSQL_USERNAME = "foxmind"
    MYSQL_PASSWORD = "Foxmind0827!"
    MYSQL_SERVER = "192.168.100.1:3306"
    DB_NAME = "foxmind"
    DB_CHARSET = "utf8"
    SQLALCHEMY_DATABASE_URI = "{JDBC_MYSQL_DRIVER}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{DB_NAME}?charset={DB_CHARSET}".format(
        JDBC_MYSQL_DRIVER=JDBC_MYSQL_DRIVER, MYSQL_DRIVER=MYSQL_DRIVER, MYSQL_USERNAME=MYSQL_USERNAME,
        MYSQL_PASSWORD=MYSQL_PASSWORD, MYSQL_SERVER=MYSQL_SERVER, DB_NAME=DB_NAME, DB_CHARSET=DB_CHARSET)

elif PROFILE == 'prod':
    SERV_PORT = 5888
    JDBC_MYSQL_DRIVER = "mysql"
    MYSQL_DRIVER = "pymysql"
    MYSQL_USERNAME = "foxmind"
    MYSQL_PASSWORD = "Foxmind0827!"
    MYSQL_SERVER = "10.209.156.141:3306"
    DB_NAME = "foxmind"
    DB_CHARSET = "utf8"
    SQLALCHEMY_DATABASE_URI = "{JDBC_MYSQL_DRIVER}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{DB_NAME}?charset={DB_CHARSET}".format(
        JDBC_MYSQL_DRIVER=JDBC_MYSQL_DRIVER, MYSQL_DRIVER=MYSQL_DRIVER, MYSQL_USERNAME=MYSQL_USERNAME,
        MYSQL_PASSWORD=MYSQL_PASSWORD, MYSQL_SERVER=MYSQL_SERVER, DB_NAME=DB_NAME, DB_CHARSET=DB_CHARSET)

if __name__ == '__main__':
    print("PYBOOT_HOME:", PYBOOT_HOME)
