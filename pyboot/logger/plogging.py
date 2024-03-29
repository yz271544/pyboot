#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: spd-sxmcc
"""
@author: lyndon
@time Created on 2018/11/13 14:20
@desc
"""
from datetime import datetime

from pyboot.conf import get_id_worker

'''Implements a simple log library.

This module is a simple encapsulation of logging module to provide a more
convenient interface to write log. The log will both print to stdout and
write to log file. It provides a more flexible way to set the log actions,
and also very simple. See examples showed below:

Example 1: Use default settings
ali
    import log

    log.debug('hello, world')
    log.info('hello, world')
    log.error('hello, world')
    log.critical('hello, world')

Result:
Print all log messages to file, and only print log whose level is greater
than ERROR to stdout. The log file is located in '/tmp/xxx.log' if the module 
name is xxx.py. The default log file handler is size-rotated, if the log 
file's size is greater than 20M, then it will be rotated.

Example 2: Use set_logger to change settings

    # Change limit size in bytes of default rotating action
    log.set_logger(limit = 10240) # 10M

    # Use time-rotated file handler, each day has a different log file, see
    # logging.handlers.TimedRotatingFileHandler for more help about 'when'
    log.set_logger(when = 'D', limit = 1)

    # Use normal file handler (not rotated)
    log.set_logger(backup_count = 0)

    # File log level set to INFO, and stdout log level set to DEBUG
    log.set_logger(level = 'DEBUG:INFO')

    # Both log level set to INFO
    log.set_logger(level = 'INFO')

    # Change default log file name and log mode
    log.set_logger(filename = 'yyy.log', mode = 'w')

    # Change default log formatter
    log.set_logger(fmt = '[%(levelname)s] %(message)s'
'''

__author__ = "tuantuan.lv <dangoakachan@foxmail.com>"
__status__ = "Development"

# __all__ = ['set_logger', 'debug', 'info', 'warning', 'error', 'critical', 'exception']

import os
import sys
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger
from enum import Enum

log_props = None

# Color escape string
COLOR_RED = '\033[1;31m'
COLOR_GREEN = '\033[1;32m'
COLOR_YELLOW = '\033[1;33m'
COLOR_BLUE = '\033[1;34m'
COLOR_PURPLE = '\033[1;35m'
COLOR_CYAN = '\033[1;36m'
COLOR_GRAY = '\033[1;37m'
COLOR_WHITE = '\033[1;38m'
COLOR_RESET = '\033[1;0m'

# Define log color
LOG_COLORS = {
    'DEBUG': '%s',
    'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
    'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
    'ERROR': COLOR_RED + '%s' + COLOR_RESET,
    'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
    'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET,
}

supported_keys = [
    'asctime',
    'created',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'message',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'thread',
    'threadName'
]

app_default_name = get_id_worker().get_id()


class FormatType(Enum):
    # 为序列值指定value值
    color = 1
    json = 2
    file = 3


class FormatKey:
    log_format = lambda x: ['%({0:s})s'.format(i) for i in x]
    standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                      '[%(levelname)s][%(message)s]',  # 其中name为getlogger指定的名字
    simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
    id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'
    simple_format_info = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    supported_format = ' '.join(log_format(supported_keys))


class ColoredFormatter(logging.Formatter):
    """
    A colorful formatter.
    """

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        rcd_dct = record.__dict__
        args = rcd_dct['args']
        lst = [e.encode('utf-8') if ['str', 'unicode'].__contains__(type(e).__name__) else e for e in args]
        new_args = tuple(lst)
        # print(new_args)
        record.__dict__['args'] = new_args
        # print(record.__dict__)
        level_name = record.levelname
        # msm = record.getMessage()
        # print(msm)
        msg = logging.Formatter.format(self, record)
        # print('aaa')
        return LOG_COLORS.get(level_name, '%s') % msg


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


class GridsumJsonFormatter(jsonlogger.JsonFormatter):

    def add_fields(self, log_record, record, message_dict):

        super(GridsumJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        if not log_record.get('production'):
            app_name = os.getenv("MY_POD_NAME")
            if app_name is not None:
                log_record['production'] = app_name
            else:
                log_record['production'] = f'pyboot-{app_default_name}'
        if log_record.get('level') in ['ERROR', 'WARNING', 'CRITICAL']:
            log_record['error_type'] = 'gridsum_error_type'
            log_record['error_msg'] = record.msg
            log_record['error_stacktrace'] = self.formatStack(record.stack_info)
        if "stack_info" in log_record:
            del log_record["stack_info"]
        if "message" in log_record:
            del log_record["message"]


class Plog:

    def __init__(self):
        self.g_logger = None

    def get_logger_instance(self):
        return self.g_logger

    def add_handler(self, cls, level, fmt, format_type, **kwargs):
        """
        Add a configured handler to the global logger.
        :param cls:
        :param level:
        :param fmt:
        :param format_type:
        :param kwargs:
        :return:
        """
        # global g_logger

        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.DEBUG)

        handler = cls(**kwargs)
        handler.setLevel(level)

        if format_type == FormatType.color:
            formatter = ColoredFormatter(fmt)
        elif format_type == FormatType.json:
            # formatter = jsonlogger.JsonFormatter()
            # formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
            # formatter = jsonlogger.JsonFormatter(format_keys())
            formatter = GridsumJsonFormatter(fmt)
        else:
            formatter = logging.Formatter(fmt)

        handler.setFormatter(formatter)
        self.g_logger.addHandler(handler)

        return handler

    @classmethod
    def update_log_props(cls, props):
        """
        Add a configured handler to the global logger.
        :param props:
        :return:
        """
        global log_props
        log_props = props

    def add_streamhandler(self, level, fmt, format_type):
        """
        Add a stream handler to the global logger.
        :param level:
        :param fmt:
        :param format_type
        :return:
        """
        return self.add_handler(logging.StreamHandler, level, fmt, format_type)

    def add_filehandler(self, level, fmt, filename, mode, backup_count, limit, when):
        """
        Add a file handler to the global logger.
        :param level:
        :param fmt:
        :param filename:
        :param mode:
        :param backup_count:
        :param limit:
        :param when:
        :return:
        """
        kwargs = {}

        # If the filename is not set, use the default filename
        if filename is None:
            filename = getattr(sys.modules['__main__'], '__file__', 'log.py')
            filename = os.path.basename(filename.replace('.py', '.log'))
            filename = os.path.join('/tmp', filename)

        kwargs['filename'] = filename

        # Choose the filehandler based on the passed arguments
        if backup_count == 0:  # Use FileHandler
            cls = logging.FileHandler
            kwargs['mode'] = mode
        elif when is None:  # Use RotatingFileHandler
            cls = logging.handlers.RotatingFileHandler
            kwargs['maxBytes'] = limit
            kwargs['backupCount'] = backup_count
            kwargs['mode'] = mode
        else:  # Use TimedRotatingFileHandler
            cls = logging.handlers.TimedRotatingFileHandler
            kwargs['when'] = when
            kwargs['interval'] = limit
            kwargs['backupCount'] = backup_count

        return self.add_handler(cls, level, fmt, False, **kwargs)

    def init_logger(self):
        """
        Reload the global logger.
        :return:
        """
        # global g_logger
        if self.g_logger is None:
            self.g_logger = logging.getLogger()
        else:
            logging.shutdown()
            self.g_logger.handlers = []
        self.g_logger.setLevel(logging.DEBUG)

    def set_logger(self, filename=None, mode='a', level='ERROR:DEBUG',
                   fmt='simple_format',
                   backup_count=5, limit=20480, when=None, format_type=FormatType.color):
        """
        Configure the global logger.
        :param filename:
        :param mode:
        :param level:
        :param fmt:
        :param backup_count:
        :param limit:
        :param when:
        :param format_type
        :return:
        """
        level = level.split(':')

        if len(level) == 1:  # Both set to the same level
            s_level = f_level = level[0]
        else:
            s_level = level[0]  # StreamHandler log level
            f_level = level[1]  # FileHandler log level

        self.init_logger()
        self.add_streamhandler(s_level, fmt, format_type)
        if filename is not None:
            self.add_filehandler(f_level, fmt, filename, mode, backup_count, limit, when)

        # Import the common log functions for convenient
        self.import_log_funcs()

    def import_log_funcs(self):
        """
        Import the common log functions from the global logger to the module.
        :return:
        """
        # global g_logger

        curr_mod = sys.modules[__name__]
        log_funcs = ['debug', 'info', 'warning', 'error', 'critical', 'exception']

        for func_name in log_funcs:
            func = getattr(self.g_logger, func_name)
            setattr(curr_mod, func_name, func)

# Set a default logger
# set_logger()
# set_logger(when='D', limit=1, level='DEBUG:INFO', filename='yyy.log', mode='w', fmt=standard_format)

# if __name__ == '__main__':
#     # import_log_funcs()
#     log = Plog()
#     standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
#                       '[%(levelname)s][%(message)s]'
#     # log.set_logger(when='D', limit=1, level='DEBUG:INFO', filename='yyy.log', mode='w', fmt=standard_format)
#     log.set_logger(when='D', limit=1, level='DEBUG:INFO', filename=None, mode='w', fmt=standard_format)
#     log.g_logger.info("123")
#     log.g_logger.error("error")
#     log.g_logger.debug('debug')
#     log.g_logger.critical('critical')
#     log.g_logger.warning('warning')
#     log.g_logger.exception('exception')
