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
@allure.story('修改用户名')
@pytest.mark.parametrize('user_success', [user_one, user_two])
def test_4201_update_user_name(user_env, user_success):
    my_user = user_env(pvg_67_conf, user_success)
    my_user.user_conf['userName'] = '张三大爷'
    my_user.update_user()
    my_user.assert_user_attr()


@allure.severity('block')
@allure.feature('用户管理')
@allure.story('修改用户角色')
@pytest.mark.parametrize('user_success', [user_one, user_two])
def test_4202_update_user_role(user_env, user_success):
    my_user = user_env(pvg_67_conf, user_success)
    my_user.user_conf['roleType'] = "ROLE_ADMIN"
    my_user.update_user()
    my_user.assert_user_attr()


