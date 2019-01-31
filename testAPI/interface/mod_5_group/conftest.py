# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言
import json
import base64
import pytest
import allure
from utils.config import Config
from utils.log import logger
from utils.sql import Sql
from testAPI.common.pre_request import PRequest
from testAPI.common.pre_sql_data import *
from testAPI.interface.mod_3_task.conftest import task_env


__all__ = (
    'APITask'
)

config_group = Config('apigroup.yml')


@pytest.fixture()
def group_api(task_env):
    my_group = APIGroup()

    def parse_api_group(groups_conf, index=0):
        my_group.parse_conf_group(task_env, groups_conf, index)
        return my_group
    yield parse_api_group
    my_group.del_group()
    assert my_group.get_group_attr("groupId") is None


@pytest.fixture(scope='module')
def group_env(task_env):
    my_group = APIGroup()
    load_group_data()

    def parse_env_group(groups_conf, index=0):
        my_group.parse_conf_group(task_env, groups_conf, index)
        my_group.groups_id = my_group.get_group_attr("groupId")
        return my_group
    yield parse_env_group


class APIGroup(PRequest):
    """
    分组接口类
    """

    def __init__(self, login=None):
        # 初始化入参
        super(APIGroup, self).__init__(login)
        # 初始化类属性
        self.group_name = None

    @allure.step('ext - 0. 预处理数据')
    def parse_conf_group(self, parse_env_task, groups_conf, index):
        self.group_conf = config_group.get(groups_conf)

        channel_id_list = []
        channel_name_list = []
        for channel_conf in self.group_conf.get('cameraNames'):
            _task_obj = parse_env_task(channel_conf)
            channel_id_list.append(_task_obj.channelId)
            channel_name_list.append(_task_obj.tasks_conf["channelName"])
            self.login = _task_obj.login

        self.group_conf["cameraIds"] = json.dumps(channel_id_list)
        self.channel_name_list = channel_name_list
        logger.debug('获取分组 "{}" 待添加设备IDs: {} '.format(self.group_name, self.group_conf["cameraIds"]))
        return

    @allure.step('ext - 1. 获取分组属性')
    def get_group_attr(self):
        pass

    @allure.step('api - 1. 添加分组')
    def save_custom_group(self, task_type, status='PASS'):

        group_list = [
          {
            "name": "2の",
            "pId": 'null',
            "id": "744FA9EC0C19470D00087D16D6839BBF",
            "isGroup": 'true',
            "taskType": 'null',
            "taskid": 'null'
          }
        ]
        api_url = "/api/video/saveCustomGroup"
        method = 'POST'
        data = {'groupList': group_list, 'type': task_type}
        self.send_request(api_url, method, status, data=data)
    
    @allure.step('api - ')
    def custom_cameras_of_group(self, status='PASS'):
        api_url = "/api/video/custom-cameras-of-group"
        method = 'GET'
        param = {'type': 'Crowd'}
        self.send_request(api_url, method, status, params=param)

    @allure.step('api - 5. 删除分组')
    def listChannelTree1(self, status='PASS'):
        api_url = "/api/video/listChannelTree1"
        method = 'POST'
        data = {'taskType': 'Crowd'}
        self.send_request(api_url, method, status, data=data)

    @allure.step('api - 5. 删除分组')
    def getTaskCustomCameraGroup(self, status='PASS'):
        api_url = "/api/video/getTaskCustomCameraGroup"
        method = 'GET'
        param = {'type': 'Crowd'}
        self.send_request(api_url, method, status, params=param)