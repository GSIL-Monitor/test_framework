# coding = utf-8
import os
import time
import pytest
import allure
from utils.config import DATA_PATH


channelName = ["crowd_channel_1", "crowd_channel_2", "crowd_channel_3", "crowd_channel_4", "crowd_channel_5", "crowd_channel_6"]
cover_default = os.path.join(DATA_PATH, 'covers', 'crowd_task_one.jpg')


@allure.severity('critical')
@allure.feature('任务配置')
@allure.story('添加删除任务')
@pytest.mark.parametrize('channel_name', channelName)
def test_3101_add_del_task(task_api, channel_name):
    my_task = task_api(channel_name)
    my_task.save_task()
    time.sleep(2)
    my_task.assert_task_status('run')


# @allure.severity('critical')
# @allure.feature('任务配置')
# @allure.story('暂停启动任务')
# def test201_update_task_status(task_api):
#     my_task = task_api(pvg_67_conf, "19、上海外滩白天", crowd_task_one)
#     my_task.save_task_covers(crowd_task_two_jpg)
#     my_task.save_task_config()
#     my_task.get_task_attr()
#
#     my_task.update_task_status('N')
#     my_task.get_task_attr()
#     my_task.assert_task_status('pause')
#     time.sleep(1)
#     my_task.update_task_status('Y')
#     my_task.get_task_attr()
#     my_task.assert_task_status('run')



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
