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
from ..mod_2_video.conftest import *
from ..conftest import *


@allure.severity('block')
@allure.feature('用户管理')
@allure.story('添加正确的用户')
@pytest.mark.parametrize('user_success', [user_one, user_two])
def test_4101_add_user(user_api, user_success):
    my_user = user_api(pvg_67_conf, user_success)
    my_user.add_user()
    my_user.assert_user_attr()
    my_user.assert_cameras()
    token = auth_login(my_user.user, my_user.password)
    auth_logout(token)

