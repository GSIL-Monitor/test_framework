# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言

import os
import time
from utils.config import Config, DATA_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.extractor import JMESPathExtractor
from utils.sql import Sql
import allure
import datetime
from ..video.conftest import *
import json
import base64
import pytest
from testAPI.common.pre_request import PRequest
from utils.support import encrypt


__all__ = (
    'user_one',
    'user_two'
)


config_video = Config('apiuser.yml')
user_one = config_video.get('user_one')
user_two = config_video.get('user_two')


@pytest.fixture()
def user_api(video_api):
    my_user = APIUser(video_api.login)

    def _user_api_setup(user_conf, video_server=None, real_count=0):
        if video_server and real_count:
            video_api.save_video(video_server)
            video_api.assert_server_count(real_count)
            channel_list = []
            sql = Sql()
            for channel_name in user_conf.get('cameraNames'):
                query_camera_count = "SELECT F_ID FROM t_video_channel " \
                                     "WHERE F_Name = '{}' " \
                                     "AND F_Video_Server_ID = '{}';".format(channel_name, video_api.server_id)
                channel_list.append(sql.query(query_camera_count)[0][0])
            user_conf["cameraIds"] = json.dumps(channel_list)

        my_user.user = user_conf["userId"]
        my_user.password = user_conf["password"]
        user_conf["password"] = encrypt(user_conf["password"])
        my_user.user_conf = user_conf
        return my_user

    yield _user_api_setup
    if my_user.id:
        my_user.delete_user()
    my_user.assert_and_get_id('FAIL')


class APIUser(PRequest):
    """
    用户接口类
    """

    def __init__(self, login):
        # 初始化入参
        super(APIUser, self).__init__(login)
        # 初始化类属性
        self.user_conf = None
        self.id = None
        self.user = None
        self.password = None

    @allure.step('api - 0. 添加用户')
    def add_user(self, status='PASS'):
        api_url = "/api/user/add-user"
        method = 'POST'
        data = self.user_conf
        self.send_request(api_url, method, status, data=data)

    @allure.step('ast - 1. 断言用户信息符合预期, 并获取用户后台唯一ID')
    def assert_and_get_id(self, status='PASS'):
        self.id = None
        for usr in self.list_user().get('rows'):
            if usr.get('uid') == self.user_conf.get('userId'):
                assert usr.get('roleType') == self.user_conf.get('roleType')
                assert usr.get('uname') == self.user_conf.get('userName')
                self.id = usr.get('id')
                break
        if status == 'FAIL' and not self.id:
            logger.info('用户{}不存在,断言成功'.format(self.user_conf.get('userId')))
        elif status == 'PASS' and self.id:
            logger.info('用户{}存在, 断言成功'.format(self.user_conf.get('userId')))
        else:
            raise AttributeError

    @allure.step('api - 1. 获取用户名称列表')
    def list_user_id_name(self, status='PASS'):
        api_url = "/api/user/list-user-id-name"
        method = 'GET'
        res = self.send_request(api_url, method, status)
        users = [user["name"] for user in res.json()]
        logger.info(users)

    @allure.step('api - 1. 获取用户概要信息列表')
    def list_user(self, status='PASS'):
        api_url = "/api/user/list-user"
        method = 'POST'
        data = {'page': 1, 'rows': 20, 'sidx': 'uid', 'sord': 'asc', 'searchString': '{"roleType":"","name":""}'}
        res = self.send_request(api_url, method, status, data=data)
        return res.json()

    @allure.step('api - 2. 获取指定用户的详细信息')
    def user_detail(self, status='PASS'):
        api_url = "/api/user/user-detail"
        method = 'POST'
        data = {'id': self.id}
        res = self.send_request(api_url, method, status, data=data, extractor='cameraRole')
        return res

    @allure.step('ast - 2. 断言用户相机权限分配符合预期')
    def assert_cameras(self):
        camera_role = self.user_detail()
        camera_list = [i.get('channelName') for i in camera_role if camera_role]
        assert set(camera_list) == set(self.user_conf.get('cameraNames'))
        logger.info('用户相机列表分配，断言成功')

    @allure.step('api - 3. 修改用户信息')
    def update_user(self, status='PASS'):
        api_url = "/api/user/update-user"
        method = 'POST'
        data = {'id': self.id, **self.user_conf}
        data.pop('userId')
        res = self.send_request(api_url, method, status, data=data)

    @allure.step('api - 4. 删除用户')
    def delete_user(self, status='PASS'):
        api_url = "/api/user/delete-user"
        method = 'POST'
        data = {'id': self.id}
        res = self.send_request(api_url, method, status, data=data)

