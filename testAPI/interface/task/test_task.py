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


@allure.severity('critical')
@allure.feature('任务配置')
@allure.story('添加删除任务')
@pytest.mark.parametrize('channel_name', channelName)
def test200_add_del_task(task_api, channel_name):
    my_task = task_api(dicts_pvg_67, crowd_task_one, channel_name, real_count_67)
    my_task.save_task_covers(crowd_task_two_jpg)
    my_task.save_task_config()
    my_task.get_task_attr()
    my_task.assert_task_status('run')


@allure.severity('critical')
@allure.feature('任务配置')
@allure.story('暂停启动任务')
def test201_update_task_status(task_api):
    my_task = task_api(dicts_pvg_67, crowd_task_one, "19、上海外滩白天", real_count_67)
    my_task.save_task_covers(crowd_task_two_jpg)
    my_task.save_task_config()
    my_task.get_task_attr()

    my_task.update_task_status('N')
    my_task.get_task_attr()
    my_task.assert_task_status('pause')
    time.sleep(1)
    my_task.update_task_status('Y')
    my_task.get_task_attr()
    my_task.assert_task_status('run')



# @allure.severity('block')
# @allure.feature('任务配置')
# @allure.story('添加任务')
# def test_add_task(login_admin):
#     my_task = APITask(login_admin, crowd_task_two)
#
#     my_task.save_task_covers(crowd_task_two_jpg)
#
#     my_task.save_task_config()
#     my_task.assert_task_status('run')
#
#     my_task.get_total_number()
#
#     my_task.get_video_param()
#
#     my_task.getTaskCustomCameraGroup()
#
#     my_task.is_enable_task()
#
#     my_task.task_config()
#
#     my_task.update_task_status()
#     my_task.assert_task_status('pause')
#
#     my_task.update_task_status()
#     my_task.assert_task_status('run')
#
#     my_task.del_task('PASS')
