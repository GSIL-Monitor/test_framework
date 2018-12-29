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
import time
import json
from utils.sql import Sql
import datetime
import pytest
import allure
from .conftest import *
from injson import check


@allure.severity('block')
@allure.feature('视频管理')
@allure.story('添加PVG服务器')
@pytest.mark.xfail(reason = '重复添加，应当失败')
@pytest.mark.parametrize('httpcode', [[200]])
def test_repeat_pvg(login_admin, init_pvg_server, httpcode):
    """重复添加"""
    msg = save_pvg_server(login_admin, init_pvg_server, httpcode)
    assert 'repeat' in msg.text



