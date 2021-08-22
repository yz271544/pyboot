import os
import sys
from pyboot.logger.plogging import Plog, FormatType, FormatKey

try:
    LOGGER_HOME = os.environ["LOGGER_HOME"]
except Exception as e:
    curPath = os.path.abspath(os.path.dirname(__file__))
    # print("settings curPath:", curPath)
    rootPath = os.path.split(curPath)[0]
    # print("settings rootPath:", rootPath)
    LOGGER_HOME = rootPath
    sys.path.append(rootPath)
    # print("settings sys.path:", sys.path)

loggerDir = 'logs'
loggerFileName = 'py-logger.log'
# stream_log_level:file_log_level
loggerLevel = 'INFO:INFO'

logFileName = LOGGER_HOME + os.sep + loggerDir + os.sep + loggerFileName
plog = Plog()

plog.set_logger(when='D', limit=1, level=loggerLevel, filename=None, mode='w',
                fmt=FormatKey.supported_format, format_type=FormatType.json)

log = plog.get_logger_instance()
