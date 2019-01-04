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

URL = Config().get('BASE_URL', index=0)


@allure.severity('blocker')
@allure.title('登录成功')
@pytest.mark.parametrize('username,password,httpcode',
                         [('admin', 'Crowd@ad123', [200]),
                          ('user', 'Crowd@us123', [200])])
def test_login_success(username, password, httpcode):
    """初始化管理员，获取token"""

    API_PATH = "/api/auth"
    METHOD = 'POST'
    JSON = {"username": username, "password": encrypt(password)}
    extractor = 'token'

    client = HTTPClient(url=(URL + API_PATH), method=METHOD)
    res = client.send(json=JSON)
    client.close()

    assert res.status_code in httpcode

    res = JMESPathExtractor().extract(extractor, res.text) if extractor else res
    return res


@allure.severity('blocker')
@allure.title('登录失败')
@pytest.mark.parametrize('username', ['admin', 'user'])
@pytest.mark.parametrize('password', ['123456', ''])
@pytest.mark.parametrize('httpcode', [[401, 405]])
def test_login_fail(username, password, httpcode):
    """使用错误密码登录失败"""

    API_PATH = "/api/auth"
    METHOD = 'POST'
    JSON = {"username": username, "password": encrypt(password)}

    client = HTTPClient(url=(URL+API_PATH), method=METHOD)
    res = client.send(json=JSON)
    client.close()

    assert res.status_code in httpcode
    assert 'Unauthorized' in res.text

    return res


if __name__ == '__main__':
    pytest.main(['test_login.py'])


