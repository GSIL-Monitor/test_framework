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
CONFIG_FILE = os.path.join(CONFIG_PATH, 'config.yml')


class Config:
    """
    读取yaml配置文件的元素
    Config(): 默认读取config/config.yml
    Config('apivideo.yml'): 读取config/apivideo.yml
    Config('testAPI/interface/video/test.yml'): 读取testAPI/interface/video/test.yml
    """

    def __init__(self, config='config.yml'):
        self.file = BASE_PATH

        if '/' in config:
            for var in config.split('/'):
                self.file = os.path.join(self.file, var)
        else:
            self.file = os.path.join(self.file, 'config', config)

        self.config = YamlReader(self.file).data

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

    VIDEO_FILE = os.path.join(BASE_PATH, 'config', 'apivideo.yml')

    dicts_pvg_67 = Config(VIDEO_FILE).get('pvg_server_67', index=1)
    real_count_67 = dicts_pvg_67.pop('real_count')
    json_pvg_67 = JSONEncoder().encode(dicts_pvg_67)

    print(json_pvg_67)

    print(real_count_67)

    config_video = Config('apitask.yml')

    task1 = config_video.get("task_one")
    camera_name = task1["channelName"]
    print(json.JSONEncoder().encode(task1))
    print(camera_name)
