# -*- coding: utf-8 -*-
"""
日志类。读取配置文件，定义日志级别、日志文件名、日志格式。
一般直接把logger import进去
from utils.log import logger
logger.info('test log')
"""
import os
import time
import logging
from utils.config import LOG_PATH, Config


class Logger(object):
    def __init__(self, logger_name='framework'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)

        _config = Config().get('log')
        # self.log_file_name = _config.get('file_name') if _config and  _config.get('file_name') else 'test.log'
        self.log_file_name = os.path.join(LOG_PATH, '{0}-{1}'.format(time.strftime('%Y-%m-%d'), _config.get('file_name')))
        # '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(_config.get('pattern'))
        self.console_output_level = _config.get('console_level')  # WARNING
        self.file_output_level = _config.get('file_level')  # INFO
        self.backup_count = _config.get('backup')  # 5

    def __logger(self, level, message):
        # 创建一个FileHandler，用于写到本地
        file_handler = logging.FileHandler(self.log_file_name, 'a', encoding='utf-8')
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(self.file_output_level)
        self.logger.addHandler(file_handler)

        # 创建一个StreamHandler,用于输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        console_handler.setLevel(self.console_output_level)
        self.logger.addHandler(console_handler)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(console_handler)
        self.logger.removeHandler(file_handler)
        # 关闭打开的文件
        file_handler.close()

    def debug(self, message):
        self.__logger('debug', message)

    def info(self, message):
        self.__logger('info', message)

    def warning(self, message):
        self.__logger('warning', message)

    def error(self, message):
        self.__logger('error', message)


logger = Logger()
if __name__ == "__main__":
    logger.info("---测试开始----")
    logger.info("操作步骤1,2,3")
    logger.warning("----测试结束----")
   






