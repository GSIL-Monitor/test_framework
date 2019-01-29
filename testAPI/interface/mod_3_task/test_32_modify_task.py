# coding = utf-8
import time
import json
from utils.sql import Sql
import datetime
import pytest
import allure
from .conftest import *
from injson import check
from ..mod_2_video.conftest import *
from utils.log import logger


@allure.severity('critical')
@allure.feature('任务配置')
@allure.story('暂停启动任务')
def test_3201_update_task_status(task_env):
    my_task = task_env(pvg_67_conf, "mbf_47", crowd_task_one)
    my_task.update_task_status('N')
    my_task.assert_task_status('pause')
    time.sleep(2)
    my_task.update_task_status('Y')
    my_task.assert_task_status('run')


