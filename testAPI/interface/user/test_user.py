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
from ..video.conftest import *
from ..conftest import *

@allure.severity('block')
@allure.feature('用户管理')
@allure.story('添加正确的用户')
@pytest.mark.parametrize('user_success', [user_one])
def test300_add_user(user_api, user_success):
    my_user = user_api(user_success, dicts_pvg_67, real_count_67)
    my_user.add_user()
    my_user.assert_and_get_id()
    my_user.assert_cameras()
    token = auth_login(my_user.user, my_user.password)
    auth_logout(token)


@allure.severity('block')
@allure.feature('用户管理')
@allure.story('修改用户名')
@pytest.mark.parametrize('user_success', [user_one, user_two])
def test301_update_user_name(user_api, user_success):
    my_user = user_api(user_success, dicts_pvg_67, real_count_67)
    my_user.add_user()
    my_user.assert_and_get_id()
    my_user.user_conf['userName'] = '张三大爷'
    my_user.update_user()


@allure.severity('block')
@allure.feature('用户管理')
@allure.story('修改用户角色')
@pytest.mark.parametrize('user_success', [user_one, user_two])
def test302_update_user_role(user_api, user_success):
    my_user = user_api(user_success, dicts_pvg_67, real_count_67)
    my_user.add_user()
    my_user.assert_and_get_id()
    my_user.user_conf['roleType'] = "ROLE_ADMIN"
    my_user.update_user()


# @allure.severity('block')
# @allure.feature('用户管理')
# @allure.story('')
# def test_add_user(user_api):
#     my_user = user_api(user_one, dicts_pvg_67, real_count_67)
#     my_user.add_user()
#     my_user.assert_and_get_id()
#     my_user.assert_cameras()
#     my_user.user_conf['userName'] = '张三大爷'
#     my_user.update_user()