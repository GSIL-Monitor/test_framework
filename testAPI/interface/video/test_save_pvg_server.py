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
from .conftest import APIVideo


@allure.severity('blocker')
@allure.feature('视频管理')
@allure.story('添加视频')
@allure.title('添加PVG视频服务器')
@pytest.mark.parametrize('pvg_server, real_count',
                         [(dicts_pvg_67, real_count_67), (dicts_pvg_10, real_count_10)], ids=['pvg67', 'pvg10'])
def test100_add_pvg(video_api, pvg_server, real_count):
    video_api.save_pvg_server(pvg_server)
    video_api.get_serverid()
    video_api.assert_server_count(real_count)


@allure.severity('blocker')
@allure.feature('视频管理')
@allure.story('添加视频')
@allure.title('添加rtsp视频')
@pytest.mark.parametrize('rtsp_server', [rtsp_server_1, rtsp_server_2])
def test101_add_rtsp(video_api, rtsp_server):
    video_api.save_rtsp(rtsp_server)
    video_api.get_serverid()


@allure.severity('normal')
@allure.feature('视频管理')
@allure.story('修改视频信息')
@allure.title('修改pvg备注信息')
def test102_rename_pvg(video_api):
    video_api.save_pvg_server(dicts_pvg_67)
    video_api.get_serverid()
    video_api.update_server_name('test_rename', '123`!@#$%^&*()', 'PVG6-7')
    video_api.update_server_name(video_api.server_name, '', 'PVG6-7')


@allure.severity('normal')
@allure.feature('视频管理')
@allure.story('修改视频信息')
@allure.title('修改rtsp备注')
@pytest.mark.parametrize('rtsp_server', [rtsp_server_1, rtsp_server_2])
def test103_rename_rtsp(video_api, rtsp_server):
    video_api.save_rtsp(rtsp_server)
    video_api.get_serverid()
    video_api.update_server_name('test_rename', '123`!@#$%^&*()', '')
    video_api.update_server_name(video_api.server_name, '', '')


@allure.severity('critical')
@allure.feature('视频管理')
@allure.story('同步pvg视频服务器')
def test104_refresh_pvg(video_api):
    video_api.save_pvg_server(dicts_pvg_67)
    video_api.get_serverid()
    video_api.refresh_pvg_server()
    video_api.assert_server_count(real_count_67)



#
# @allure.severity('block')
# @allure.feature('视频管理')
# @allure.story('添加PVG服务器')
# @pytest.mark.xfail(reason='重复添加，应当失败')
# def test_repeat_pvg(login_admin):
#     """重复添加"""
#     av = APIVideo(login_admin)
#     av.save_pvg_server('PASS', dicts_pvg_67)
#     av.list_channel_tree_new('PASS')
#     av.get_serverid()
#
#     av.assert_server_count(real_count_67)
#
#     av.refresh_pvg_server('PASS')
#     av.assert_server_count(real_count_67)
#
#     server = av.video_server_detail('PASS')
#     logger.info(check(dicts_pvg_67, server.json()))
#
#     av.update_server_name('PASS', 'test_rename', '123`!@#$%^&*()', 'PVG6-7')
#
#     av.update_server_name('PASS', av.server_name, '', 'PVG6-7')
#
#     av.get_enable_task_count_by_videoserver('PASS')
#
#     av.save_rtsp('PASS', rtsp_server_1)
#     av.save_rtsp('PASS', rtsp_server_2)
#
#     av.del_video_server('PASS')
#
