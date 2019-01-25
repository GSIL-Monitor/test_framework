# coding = utf-8

"""
api-接口请求， ext-结果提取处理， ast-自定义断言
"""

import os
import time
import unittest
from utils.config import Config, REPORT_PATH, DATA_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
from utils.support import encrypt
from utils.mail import Email
import time
import json
from utils.sql import Sql
import datetime
import pytest
import allure_pytest
import allure
from utils.extractor import JMESPathExtractor
import time
from testAPI.common.pre_request import PRequest


__all__ = ('base_url',
           'license_right',
           'license_wrong',
           'APIAuth'
           )

base_url = Config().get('BASE_URL', index=0)
license_right = '{}.license_key'.format(base_url.partition("://")[-1])
license_wrong = 'error.license_key'


@pytest.fixture()
def auth_api(login_admin):
    auth = APIAuth(login_admin)
    yield auth


class APIAuth(PRequest):
    """
    登录授权类
    """

    def __init__(self, login):
        """
        1. 继承父类构造函数，获取登录token，传递给自定义接口请求函数self.send_request
        2. 初始化类属性
        """
        super(APIAuth, self).__init__(login)

    @allure.step('api - 获取硬件信息')
    def get_hard_ware_info(self, status='PASS'):
        api_url = "/api/crowd-auth/get-hard-ware-info"
        method = 'POST'
        res = self.send_request(api_url, method, status)
        return res

    @allure.step('api - 导入授权')
    def set_auth_key(self, license, status='PASS'):
        api_url = "/api/crowd-auth/set-auth-key"
        method = 'POST'
        license_file = os.path.join(DATA_PATH, 'license', license)
        res = self.send_request(api_url, method, status, files={'license': open(license_file, 'rb')})
        return res

    @allure.step('api - 获取授权状态')
    def get_auth_info(self, status='PASS'):
        api_url = "/api/crowd-auth/get-auth-info"
        method = 'POST'
        extractor = 'ext'
        res = self.send_request(api_url, method, status, extractor=extractor)
        return res

