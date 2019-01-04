"""
读取配置。采用yaml格式配置文件，也可以采用xml、ini等，需要在file_rader添加响应Reader处理。
"""
import os
from utils.file_reader import YamlReader
import json
from json import JSONEncoder

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_PATH = os.path.join(BASE_PATH, 'config')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVERS_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'reports')
# TEST_PATH = os.path.join(BASE_PATH, 'test')
# UTILS_PATH = os.path.join(BASE_PATH,'utils')
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')


class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index=0):
        """
        get config element
        :param element: yaml element
        :param index: yaml is separated to lists by '---'
        :return:
        """
        return self.config[index].get(element)



if __name__ == '__main__':
    c = Config()
    print(c.get('URL'), BASE_PATH)

    dicts_pvg_67 = Config().get('pvg_server_67', index=1)
    real_count_67 = dicts_pvg_67.pop('real_count')
    json_pvg_67 = JSONEncoder().encode(dicts_pvg_67)

    print(json_pvg_67)

    print(real_count_67)


