# coding = utf-8
import pytest
import allure
from .conftest import *


@allure.severity('normal')
@allure.feature('视频管理')
@allure.story('修改视频信息')
@allure.title('修改pvg备注信息')
def test_2201_rename_pvg(video_env):
    my_video = video_env(pvg_67_conf)
    my_video.update_server_name('test_rename', '123`!@#$%^&*()', 'PVG6-7')
    my_video.update_server_name(my_video.server_name, '', 'PVG6-7')


@allure.severity('normal')
@allure.feature('视频管理')
@allure.story('修改视频信息')
@allure.title('修改rtsp备注')
@pytest.mark.parametrize('rtsp_server', [rtsp_server_1, rtsp_server_2])
def test_2202_rename_rtsp(video_env, rtsp_server):
    my_video = video_env(rtsp_server)
    my_video.update_server_name('test_rename', '123`!@#$%^&*()', '')
    my_video.update_server_name(my_video.server_name, '', '')


@allure.severity('critical')
@allure.feature('视频管理')
@allure.story('同步pvg视频服务器')
def test_2203_refresh_pvg(video_env):
    my_video = video_env(pvg_67_conf)
    my_video.refresh_pvg_server()
    my_video.assert_server_count(real_count_67)

