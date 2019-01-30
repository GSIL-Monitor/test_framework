# coding = utf-8
import time
import allure
import pytest


@allure.severity('critical')
@allure.feature('任务配置')
@allure.story('暂停启动任务')
def test_3201_update_task_status(task_env):
    my_task = task_env(video_server='pvg_server_67', channel_name="mbf_47", tasks_conf='crowd_template_one')
    my_task.update_task_status('N')
    my_task.assert_task_status('pause')
    time.sleep(2)
    my_task.update_task_status('Y')
    my_task.assert_task_status('run')


