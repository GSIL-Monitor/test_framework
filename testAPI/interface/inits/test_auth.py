# coding = utf-8
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

URL = Config().get('BASE_URL', index=0)
license_right = '{}.license_key'.format(URL.partition("://")[-1])
license_wrong = 'error.license_key'


@allure.step('导入授权')
def set_auth_key(login_admin, license):

    API_PATH = "/api/crowd-auth/set-auth-key"
    METHOD = 'POST'
    headers = {'Authorization': login_admin}

    client = HTTPClient(url=(URL + API_PATH), method=METHOD, headers=headers)

    license_file = os.path.join(DATA_PATH, 'license', license)
    res = client.send(files={'license': open(license_file, 'rb')})
    return res


@allure.step('获取授权状态')
def get_auth_info(login_admin):

    API_PATH = "/api/crowd-auth/get-auth-info"
    METHOD = 'POST'
    headers = {'Authorization': login_admin}

    client = HTTPClient(url=(URL + API_PATH), method=METHOD, headers=headers)

    res = client.send()
    return res


@allure.severity('blocker')
@allure.feature('授权管理')
@allure.story('导入授权')
@pytest.mark.parametrize('title,license,ext',
                         [('1授权导入成功', license_right, '16'), ('2授权导入失败', license_wrong, '0')]
                         )
def test_set_auth_key(login_admin, title, license, ext):
    """授权导入测试"""
    allure.dynamic.title(title)

    res0 = set_auth_key(login_admin, license)
    assert res0.status_code in [200]

    time.sleep(3)

    extractor = 'ext'
    res1 = get_auth_info(login_admin)
    res1 = JMESPathExtractor().extract(extractor, res1.text) if extractor else res1
    assert res1 == ext

