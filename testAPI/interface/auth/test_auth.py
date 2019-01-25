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
from .conftest import *
import time
from .conftest import *


@allure.severity('blocker')
@allure.feature('授权管理')
@allure.story('导入授权')
@allure.title('授权导入失败')
def test010_set_auth_wrong(auth_api):
    """授权导入测试"""
    auth_api.set_auth_key(license_wrong)
    time.sleep(3)
    res = auth_api.get_auth_info()
    assert res == '0'


@allure.severity('blocker')
@allure.feature('授权管理')
@allure.story('导入授权')
@allure.title('授权导入成功')
def test011_set_auth_right(auth_api):
    """授权导入测试"""
    auth_api.set_auth_key(license_right)
    time.sleep(3)
    res = auth_api.get_auth_info()
    assert res == '16'


@allure.severity('blocker')
@allure.feature('授权管理')
@allure.story('获取硬件信息')
def test012_get_auth_key(auth_api):
    """硬件信息"""
    auth_api.get_hard_ware_info()



