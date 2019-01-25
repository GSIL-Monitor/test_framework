# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言

import os
import time
from utils.config import Config, DATA_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.extractor import JMESPathExtractor
from utils.sql import Sql
import allure
import datetime
from ..video.conftest import *
import json
import base64
import pytest
from testAPI.common.pre_request import PRequest

__all__ = ('base_url',
           'APITask',
           'crowd_task_one',
           'crowd_task_two',
           'crowd_task_one_jpg',
           'crowd_task_two_jpg',
           'channelName'
           )

base_url = Config().get('BASE_URL', index=0)

config_video = Config('apitask.yml')
crowd_task_one = config_video.get("crowd_task_one")
crowd_task_two = config_video.get("crowd_task_two")

crowd_task_one_jpg = os.path.join(DATA_PATH, 'covers', 'crowd_task_one.jpg')
crowd_task_two_jpg = os.path.join(DATA_PATH, 'covers', 'crowd_task_two.jpg')

channelName = ["19、上海外滩白天", "20、上海外滩夜晚", "mbf_47", "mbf_26",
               "24、人群通道效果", "10.0.10.200"]


@pytest.fixture()
def task_api(video_api):
    my_task = APITask(video_api.login)

    def _task_api_setup(video_server, tasks_conf, channel_name, real_count=0, task_name=None):
        video_api.save_video(video_server)
        if real_count:
            video_api.assert_server_count(real_count)
        logger.debug(channel_name)
        logger.debug(tasks_conf)
        query_camera_count = "SELECT F_ID FROM t_video_channel " \
                             "WHERE F_Name = '{}' " \
                             "AND F_Video_Server_ID = '{}';".format(channel_name, video_api.server_id)
        tasks_conf["channelId"] = Sql().query(query_camera_count)[0][0]
        tasks_conf["channelName"] = channel_name
        tasks_conf["taskName"] = task_name if task_name else channel_name
        logger.info('获取相机"{}"的ID为{}'.format(channel_name, tasks_conf["channelId"]))
        my_task.tasks_conf = tasks_conf
        my_task.channelId = tasks_conf["channelId"]
        return my_task

    yield _task_api_setup
    if my_task.tasks_id:
        my_task.del_task()
    my_task.get_task_attr()
    assert my_task.tasks_id is None


class APITask(PRequest):
    """
    任务接口类
    """

    def __init__(self, login):
        # 初始化入参
        super(APITask, self).__init__(login)
        # 初始化类属性
        self.tasks_conf = None
        self.channelId = None
        self.tasks_type = 'Crowd'
        self.tasks_id = None
        self.tasks_key = 0
        self.tasks_status = None
        self.total_tasks = 0

    @allure.step('api - 1. 上传封面')
    def save_task_covers(self, cover_image, status='PASS'):
        api_url = "/api/task/save-task-covers"
        method = 'POST'

        data = {'channelId': self.channelId, 'base64': base64.b64encode(open(cover_image, 'rb').read())}
        res = self.send_request(api_url, method, status, data=data)
        logger.info("{}".format(res.json()))

    @allure.step('api - 2. 添加任务')
    def save_task_config(self, tasks_type='Crowd', status='PASS'):
        api_url = "/api/task/save-task-config"
        method = 'POST'
        data = {'taskType': tasks_type, 'jsonParam': json.JSONEncoder().encode(self.tasks_conf)}
        self.send_request(api_url, method, status, data=data)
        self.tasks_type = tasks_type

    @allure.step('api - 3.1 查询任务列表')
    def list_task(self, status='PASS'):
        api_url = "/api/task/list-task"
        method = 'POST'
        data = {'searchString': '{}'.format({"taskType": self.tasks_type}),
                '_search': 'false',
                'nd': 1547123232576,
                'rows': 10,
                'page': 1,
                'sord': 'asc',
                'sidx': None
                }
        res = self.send_request(api_url, method, status, data=data, extractor='rows')
        logger.info('tasks_lists: {}'.format(res))
        return res

    @allure.step('ext - 3.2 获取任务ID/KEY/STATUS/TOTOAL_NUM')
    def get_task_attr(self):
        """
        每次任务更新都要执行这句话：增加、修改、启停、删除
        可以获得任务的最新状态、最新ID、最新KEY、最新任务总数
        """
        tasks_list_json = self.list_task()
        num = 0
        for row in tasks_list_json:
            for col in row.values():
                if col.get("channelId") == self.channelId:
                    self.tasks_id, self.tasks_key, self.tasks_status = col.get("taskId"), col.get("taskKey"), col.get("status")
                    break
                else:
                    self.tasks_id = self.tasks_key = self.tasks_status = None
            if row.get("column2"):
                num += 2
            elif row.get("column1"):
                num += 1
                break
            else:
                break
        self.total_tasks = num
        logger.info('task_id: {}'.format(self.tasks_id))
        logger.info('tasks_key: {}'.format(self.tasks_key))
        logger.info('tasks_status: {}'.format(self.tasks_status))
        logger.info('total_tasks_num: {}'.format(self.total_tasks))

    @allure.step('ast - 3. 断言任务状态')
    def assert_task_status(self, tasks_status='run'):
        assert self.tasks_status == tasks_status

    @allure.step('api - 4. 获取任务配置详细信息')
    def get_task_config(self, status='PASS'):
        api_url = "/api/task/task-config"
        method = 'POST'
        data = {'channelId': self.channelId, 'taskType': self.tasks_type,
                'videoSize': '{"videoType": 1, "width": 1920, "height": 1080, "duration": 0}'
                }
        res = self.send_request(api_url, method, status, data=data)
        logger.info("{}".format(res.json()))

    @allure.step('api - 4. 取流')
    def get_video_param(self, status='PASS'):
        api_url = "/api/video/get-video-param?" \
                  "type=noFourScreen&channelId={}&taskType=Crowd".format(self.channelId)
        method = 'POST'
        res = self.send_request(api_url, method, status, extractor='ext')
        channel_info = base64.b64decode(res)
        logger.info("video param: {}".format(channel_info))

    @allure.step('api - 4. 获取任务状态？什么都没有')
    def is_enable_task(self, status='PASS'):
        api_url = "/api/task/is-enable-task"
        method = 'POST'
        data = {'taskType': 'Crowd'}
        res = self.send_request(api_url, method, status, data=data)
        logger.info("{}".format(res.json()))

    @allure.step('api - 4. 获取任务相机分组？有任务和相机的ID，任务和分组的名称，所属的视频服务')
    def getTaskCustomCameraGroup(self, status='PASS'):
        api_url = "/api/video/getTaskCustomCameraGroup"
        method = 'GET'
        params = {'type': 'Crowd'}
        res = self.send_request(api_url, method, status, params=params)
        logger.info("{}".format(res.json()))

    @allure.step('api - 4. 启停任务')
    def update_task_status(self, ignition='Y', status='PASS'):
        api_url = "/api/task/update-task-status"
        method = 'POST'
        data = {'taskId': self.tasks_id, 'status': ignition}
        res = self.send_request(api_url, method, status, data=data)
        logger.info("{}".format(res.json()))

    @allure.step('api - 4. 恢复上次配置')
    def use_last_config(self, tasks_type='Crowd', last_conf=None, status='PASS'):
        api_url = "/api/task/use-last-config"
        method = 'POST'
        data = {'channelId': self.channelId, 'taskType': tasks_type}
        res = self.send_request(api_url, method, status, data=data, extractor='task')
        logger.info("{}".format(res.json()))

    @allure.step('api - 5. 删除任务')
    def del_task(self, status='PASS'):
        api_url = "/api/task/del-task"
        method = 'POST'
        data = {'taskId': self.tasks_id}
        res = self.send_request(api_url, method, status, data=data)
        logger.info("{}".format(res.json()))


