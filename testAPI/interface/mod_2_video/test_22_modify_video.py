# coding = utf-8
import pytest
import allure


@allure.severity('normal')
@allure.feature('视频管理')
@allure.story('修改视频信息')
@allure.title('修改pvg备注信息')
def test_2201_rename_pvg(video_env):
    my_video = video_env('pvg_server_67')
    my_video.update_server_name('test_rename', '123`!@#$%^&*()', 'PVG6-7')


@allure.severity('normal')
@allure.feature('视频管理')
@allure.story('修改视频信息')
@allure.title('修改rtsp备注')
def test_2202_rename_rtsp(video_env):
    my_video = video_env('rtsp_server_1')
    my_video.update_server_name('test_rename', '123`!@#$%^&*()', '')


@allure.severity('critical')
@allure.feature('视频管理')
@allure.story('同步pvg视频服务器')
@pytest.mark.parametrize('pvg_server', ['pvg_server_67', 'pvg_server_10'], ids=['1-pvg67', '2-pvg10'])
def test_2203_refresh_pvg(video_env, pvg_server):
    my_video = video_env(pvg_server)
    my_video.refresh_pvg_server()
    my_video.assert_server_count()

