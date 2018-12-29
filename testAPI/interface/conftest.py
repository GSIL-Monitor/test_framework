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
from utils.extractor import JMESPathExtractor

URL = Config().get('BASE_URL', index=0)


@pytest.fixture(scope='session')
def login_admin(request):
    """初始化管理员，获取token"""

    API_PATH = "/api/auth"
    METHOD = 'POST'
    JSON = {"username": 'admin', "password": encrypt('Crowd@ad123')}
    httpcode = [200]
    extractor = 'token'

    client = HTTPClient(url=(URL+API_PATH), method=METHOD)
    res = client.send(json=JSON)

    assert res.status_code in httpcode

    res = JMESPathExtractor().extract(extractor, res.text) if extractor else res
    yield res

    request.addfinalizer(client.close)  # close()不加括弧


# class DB(object):
#     def __init__(self):
#         self.intransaction = {}
#
#     def set(self, api, value):
#         self.intransaction[api] = value
#
# @pytest.fixture
# def db():
#     return DB()
#
#
# @pytest.fixture
# def transact(request, db):
#     yield
#     api = request.function.__name__
#     value = getattr(request.module, 'res')
#     db.set(api, value)




