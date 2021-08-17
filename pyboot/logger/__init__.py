import os
import sys
from pyboot.logger.plogging import Plog

try:
    LOGGER_HOME = os.environ["LOGGER_HOME"]
except Exception as e:
    curPath = os.path.abspath(os.path.dirname(__file__))
    print("settings curPath:", curPath)
    rootPath = os.path.split(curPath)[0]
    print("settings rootPath:", rootPath)
    LOGGER_HOME = rootPath
    sys.path.append(rootPath)
    print("settings sys.path:", sys.path)

loggerDir = 'logs'
loggerFileName = 'py-logger.log'
loggerLevel = 'DEBUG:INFO'
loggerFormat = 'standard_format'
logFormatDict = {
    'standard_format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                       '[%(levelname)s][%(message)s]',  # 其中name为getlogger指定的名字
    'simple_format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s',
    'id_simple_format': '[%(levelname)s][%(asctime)s] %(message)s',
    'simple_format_info': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}
logFileName = LOGGER_HOME + os.sep + loggerDir + os.sep + loggerFileName
plog = Plog()
plog.set_logger(when='D', limit=1, level=loggerLevel, filename=None, mode='w',
                fmt=logFormatDict[loggerFormat])

log = plog.get_logger_instance()
