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

URL = Config().get('BASE_URL', index=0)
video = [('10.0.100.12', 150)]


@allure.severity('block')
@allure.feature('视频管理')
@allure.story('同步PVG服务器')
@pytest.mark.parametrize('video_name, real_count', video)
@pytest.mark.parametrize('httpcode', [[200]])
def test_refresh_pvg(login_admin, init_pvg_server, video_name, real_count, httpcode):
    """同步PVG服务器"""
    server_id = list_channel_tree_new(video_name, httpcode)
    refresh_pvg_server(login_admin, server_id, httpcode)
    assert_server_count(server_id, real_count)

