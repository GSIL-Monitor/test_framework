# coding = utf-8
import os
import time
import unittest
from utils.config import Config, REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
from utils.support import encrypt
from utils.mail import Email
import pytest
import allure_pytest
import allure
from utils.extractor import JMESPathExtractor
from testAPI.interface.conftest import *


@allure.severity('blocker')
@allure.feature('登入登出')
@allure.story('登入')
@allure.title('登录成功')
@pytest.mark.parametrize('username, password, status',
                         [('admin', 'Crowd@ad123', 'PASS'),
                          ('user', 'Crowd@us123', 'PASS')])
def test000_login_success(username, password, status):
    """登陆成功"""
    auth_login(username, password, status)


@allure.severity('blocker')
@allure.feature('登入登出')
@allure.story('登入')
@allure.title('登录失败')
@pytest.mark.parametrize('username', ['admin', 'user'])
@pytest.mark.parametrize('password', ['123456', ''])
@pytest.mark.parametrize('status', ['FAIL'])
def test001_login_fail(username, password, status):
    """使用错误密码登录失败"""
    res = auth_login(username, password, status)
    assert 'Unauthorized' in res.text


if __name__ == '__main__':
    pytest.main(['test_login.py'])


