# coding = utf-8
import os
import time
import pytest
import allure
from utils.config import DATA_PATH
from utils.log import logger


cover_default = os.path.join(DATA_PATH, 'covers', 'crowd_task_one.jpg')


@allure.severity('critical')
@allure.feature('任务配置')
@allure.story('暂停启动任务')
def test_3201_update_task_status(task_env):
    my_task = task_env("crowd_channel_5")
    my_task.update_task_status('N')
    my_task.assert_task_status('pause')
    time.sleep(2)
    my_task.update_task_status('Y')
    my_task.assert_task_status('run')


@allure.severity('critical')
@allure.feature('任务配置')
@allure.story('修改任务名称')
@pytest.mark.parametrize('task_rename', ["rename_task"])
def test_3202_update_task_name(task_env, task_rename):
    my_task = task_env("crowd_channel_5")
    my_task.tasks_conf["taskName"] = task_rename
    my_task.save_task()
    time.sleep(2)
    assert my_task.get_task_attr("taskName") == task_rename
    my_task.assert_task_status('run')


@allure.severity('critical')
@allure.feature('播放视频')
@allure.story('取流信息匹配')
def test_3203_get_video_param(task_env):
    my_task = task_env("crowd_channel_2")
    channel_info = my_task.get_video_param()
    assert str(channel_info) is not None


@allure.severity('critical')
@allure.feature('地图坐标')
def test_3204_map_coordinate(task_env):
    my_task = task_env("crowd_channel_2")
    my_task.update_coordinate('[22.2222, 19.9999]')
    assert my_task.channel_detail() == '[22.2222, 19.9999]'
    my_task.update_coordinate('')
    assert not my_task.channel_detail()


@allure.severity('critical')
@allure.feature('坐标导出和导入')
def test_3205_exp_coordinate(task_env):
    my_task = task_env("crowd_channel_2")
    my_task.exp_coordinates()
    my_task.imp_coordinates()
