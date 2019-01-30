# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言
import json
import base64
import pytest
import allure
from utils.config import Config
from utils.log import logger
from utils.sql import Sql
from testAPI.common.pre_request import PRequest
from testAPI.common.pre_sql_data import *
from ..mod_2_video.conftest import *


__all__ = (
    'APITask'
)

config_task = Config('apitask.yml')


@pytest.fixture()
def task_api(video_env):
    my_task = APITask()

    def parse_api_task(video_server, channel_name, tasks_conf, index=0, tasks_type='Crowd', task_name=None):
        my_video = video_env(video_server)
        my_task.login = my_video.login
        my_task.parse_conf_task(my_video.server_id, channel_name, tasks_conf, index, tasks_type, task_name)
        return my_task

    yield parse_api_task
    my_task.del_task()
    assert my_task.get_task_attr("taskId") is None


@pytest.fixture(scope='module')
def task_env(video_env):
    my_task = APITask()
    load_task_data()

    def parse_env_task(video_server, channel_name, tasks_conf, index=0, tasks_type='Crowd', task_name=None):
        my_video = video_env(video_server)
        my_task.login = my_video.login
        my_task.parse_conf_task(my_video.server_id, channel_name, tasks_conf, index, tasks_type, task_name)
        my_task.tasks_id = my_task.get_task_attr("taskId")
        return my_task
    yield parse_env_task


class APITask(PRequest):
    """
    任务接口类
    """

    def __init__(self, login=None):
        # 初始化入参
        super(APITask, self).__init__(login)
        # 初始化类属性
        self.tasks_conf = None
        self.channelId = None
        self.tasks_type = None
        self.tasks_id = None
        self.flag = 0

    @allure.step('ext - 0. 预处理数据，初始化任务基本信息<设备ID/名称,任务名称>')
    def parse_conf_task(self, server_id, channel_name, tasks_conf, index=0, tasks_type='Crowd', task_name=None):
        self.tasks_conf = config_task.get(tasks_conf, index)
        self.tasks_type = tasks_type
        self.flag = index
        self.tasks_conf["channelName"] = channel_name
        self.tasks_conf["taskName"] = task_name if task_name else channel_name
        mysql = Sql()
        query_camera_id = "SELECT F_ID FROM t_video_channel " \
                          "WHERE F_Name = '{}' " \
                          "AND F_Video_Server_ID = '{}';".format(channel_name, server_id)
        req = mysql.query(query_camera_id)
        mysql.close()
        if req:
            self.channelId = self.tasks_conf["channelId"] = req[0][0]
            logger.debug('获取相机"{}"的ID为{}'.format(channel_name, self.channelId))
        else:
            raise ValueError('错误：相机{}不存在'.format(channel_name))
        return

    @allure.step('ext - 1. 添加任务获取ID <上传封面--添加任务--任务ID> ')
    def save_task(self, cover_image, status='PASS'):
        self.save_task_covers(cover_image, status)
        self.save_task_config(status)
        self.tasks_id = self.get_task_attr("taskId")
        assert self.tasks_id is not None
        # yml文件以'---'分割，第一章节(index==0)为有效用例(断言成功），后续章节(index!=0)为无效用例（断言失败）
        assert self.tasks_id is None if self.flag else self.tasks_id is not None

    @allure.step('api - 1. 上传封面')
    def save_task_covers(self, cover_image, status='PASS'):
        api_url = "/api/task/save-task-covers"
        method = 'POST'

        data = {'channelId': self.channelId, 'base64': base64.b64encode(open(cover_image, 'rb').read())}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug("{}".format(res.json()))

    @allure.step('api - 2. 添加任务')
    def save_task_config(self, status='PASS'):
        api_url = "/api/task/save-task-config"
        method = 'POST'
        data = {'taskType': self.tasks_type, 'jsonParam': json.JSONEncoder().encode(self.tasks_conf)}
        self.send_request(api_url, method, status, data=data)

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

    @allure.step('ext - 3.2 获取任务属性')
    def get_task_attr(self, *tasks_attr):
        """
        每次任务更新都要执行这句话：增加、修改、启停、删除
        根据唯一设备ID，获得对应任务的最新状态、最新ID、最新KEY
        >>>self.get_task_attr("taskId")
        >>>self.get_task_attr("taskKey")
        >>>self.get_task_attr("status")
        >>>self.get_task_attr("taskId", "taskKey", "status")
        """
        tasks_list_json = self.list_task()
        for row in tasks_list_json:
            for col in row.values():
                if col.get("channelId") == self.channelId:
                    val = [col.get(attr) for attr in tasks_attr]
                    logger.debug('获取任务{}属性: {} = {} '.format(self.tasks_conf["taskName"], tasks_attr, val))
                    return val[0] if len(val) == 1 else val
        val = [None for attr in tasks_attr]
        return val[0] if len(val) == 1 else val

    @allure.step('ext - 3. 获取任务总数')
    def get_total_num(self):
        task_num = 0
        tasks_list_json = self.list_task()
        for row in tasks_list_json:
            if row.get("column2"):
                task_num += 2
            elif row.get("column1"):
                task_num += 1
                break
            else:
                break
        logger.info('total_tasks_num: {}'.format(task_num))
        return task_num

    @allure.step('ast - 3. 断言任务状态')
    def assert_task_status(self, tasks_status='run'):
        real_status = self.get_task_attr("status")
        assert real_status == tasks_status

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


