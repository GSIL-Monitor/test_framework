# coding = utf-8
import pytest
import allure


@allure.severity('blocker')
@allure.feature('视频管理')
@allure.story('添加视频')
@allure.title('添加PVG视频服务器成功')
@pytest.mark.parametrize('pvg_server', ['pvg_server_67', 'pvg_server_10'], ids=['1-pvg67', '2-pvg10'])
def test_2101_add_pvg(video_api, pvg_server):
    # 添加
    video_api.save_video(pvg_server)
    video_api.assert_server_count()
    # 删除
    video_api.del_video_server()
    assert video_api.query_video_id() is None


@allure.severity('blocker')
@allure.feature('视频管理')
@allure.story('添加视频')
@allure.title('添加rtsp视频成功')
@pytest.mark.parametrize('rtsp_server', ['rtsp_server_1', 'rtsp_server_2'])
def test_2102_add_rtsp(video_api, rtsp_server):
    # 添加
    video_api.save_video(rtsp_server)
    # 删除
    video_api.del_rtsp_video()
    assert video_api.query_video_id() is None


@allure.severity('blocker')
@allure.feature('视频管理')
@allure.story('添加视频')
@allure.title('添加PVG视频服务器失败')
@pytest.mark.parametrize('pvg_server',
                         ['pvg_server_67_1', 'pvg_server_67_2', 'pvg_server_67_3','pvg_server_67_4', 'pvg_server_67_5',
                          'pvg_server_10_1', 'pvg_server_10_2', 'pvg_server_10_3', 'pvg_server_10_4', 'pvg_server_10_5'])
def test_2101_add_pvg_name_fail(video_api, pvg_server):
    video_api.save_video(pvg_server, index=1)






#
# @allure.severity('block')
# @allure.feature('视频管理')
# @allure.story('添加PVG服务器')
# @pytest.mark.xfail(reason='重复添加，应当失败')
# def test_repeat_pvg(login_admin):
#     """重复添加"""
#     av = APIVideo(login_admin)
#     av.save_pvg_server('PASS', pvg_67_conf)
#     av.list_channel_tree_new('PASS')
#     av.get_serverid()
#
#     av.assert_server_count(real_count_67)
#
#     av.refresh_pvg_server('PASS')
#     av.assert_server_count(real_count_67)
#
#     server = av.video_server_detail('PASS')
#     logger.info(check(pvg_67_conf, server.json()))
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
