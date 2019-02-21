# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言
import json
import pytest
import allure
import time
from utils.config import Config
from utils.log import logger
from utils.sql import Sql
from utils.support import encrypt
from testAPI.common.pre_request import PRequest
from testAPI.common.pre_sql_data import *
from testAPI.interface import conftest


__all__ = (
    'APIStatus'
)


@pytest.fixture(scope='session')
def status_api(login_admin, task_env):
    my_status = APIStatus(login_admin)
    load_group_data()

    def parse_api_status(*channel):
        my_status.channel_ids = [task_env(ch).channelId for ch in channel]
        return my_status
    return parse_api_status


class APIStatus(PRequest):
    """
    用户接口类
    """

    def __init__(self, login=None):
        # 初始化入参
        super(APIStatus, self).__init__(login)
        # 初始化类属性
        self.channel_ids = None
        self.groupIds = None

    @allure.step('api - 1. 人群分组实时状态')
    def status_group(self, status='PASS'):
        api_url = "/api/realstatus/groupList"
        method = 'POST'
        data = {'nd': int(time.time()*1000), 'sidx': 'channelName', 'sord': 'asc', 'page': 1, 'rows': 5, '_search': 'false'}
        res = self.send_request(api_url, method, status, data=data)
        return res.json()

    @allure.step('api - 2. 人群相机实时状态')
    def status_channel(self, status='PASS'):
        api_url = "/api/realstatus/list"
        method = 'POST'
        data = {'cameraIds': ','.join(self.channel_ids), 'nd': int(time.time()*1000), 'sidx': 'channelName', 'sord': 'asc',
                'page': 1, 'rows': 5, '_search': 'false'}
        res = self.send_request(api_url, method, status, data=data)
        return res.json()

    @allure.step('api - 3. 跨线分组实时状态')
    def status_group_cross(self, status='PASS'):
        api_url = "/api/realstatus/crossLineGroupList"
        method = 'POST'
        data = {'nd': int(time.time()*1000), 'sidx': 'name', 'sord': 'asc', 'page': 1, 'rows': 10000, '_search': 'false'}
        res = self.send_request(api_url, method, status, data=data)
        return res.json()

    @allure.step('api - 4. 跨线相机实时状态')
    def status_channel_cross(self, status='PASS'):
        api_url = "/api/realstatus/crossline"
        method = 'POST'
        data = {'cameraIds': ','.join(self.channel_ids), 'nd': int(time.time()*1000), 'sidx': 'cameraName', 'sord': 'asc',
                'page': 1, 'rows': 5, '_search': 'false'}
        res = self.send_request(api_url, method, status, data=data)
        return res.json()
