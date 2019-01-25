# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言

import time
from utils.config import Config
from utils.log import logger
from utils.sql import Sql
import allure
import datetime
from testAPI.common.pre_request import PRequest
import pytest

__all__ = ('base_url',
           'dicts_pvg_67',
           'dicts_pvg_10',
           'real_count_67',
           'real_count_10',
           'rtsp_server_1',
           'rtsp_server_2',
           'APIVideo',
           'video_api'
           )

base_url = Config().get('BASE_URL', index=0)

config_video = Config('apivideo.yml')

dicts_pvg_67 = config_video.get('pvg_server_67', index=0)
real_count_67 = dicts_pvg_67.pop('real_count')
dicts_pvg_10 = config_video.get('pvg_server_10', index=0)
real_count_10 = dicts_pvg_10.pop('real_count')

rtsp_server_1 = config_video.get('rtsp_server_1', index=0)
rtsp_server_2 = config_video.get('rtsp_server_2', index=0)


@pytest.fixture()
def video_api(login_admin):
    av = APIVideo(login_admin)
    yield av
    av.get_serverid()
    if av.server_id:
        av.del_video_server()


class APIVideo(PRequest):
    """
    视频接口类
    """

    def __init__(self, login):
        """
        1. 继承父类构造函数，获取登录token，传递给自定义接口请求函数self.send_request
        2. 初始化类属性（名称、ID、子设备数）
        """
        super(APIVideo, self).__init__(login)
        self.server_name = None
        self.server_id = None
        self.real_count = 0
        self.channel_tree = None

    @allure.step('ext - 合并添加视频服务器的两个接口为一个方法：添加视频')
    def save_video(self, video_server):
        # 初始化视频服务器，获取视频服务器ID、相机ID
        if video_server.get('version') == 'rtsp':
            self.save_rtsp(video_server)
        else:
            self.save_pvg_server(video_server)
        self.get_serverid()

    @allure.step('api - 1. 添加rtsp视频')
    def save_rtsp(self, rtsp_json, status='PASS'):
        api_url = "/api/video/save-rtsp"
        method = 'POST'
        data = {'rtspUrl': rtsp_json['url'], 'rtspName': rtsp_json['name']}
        res = self.send_request(api_url, method, status, data=data)

        self.server_name = 'rtsp视频'
        logger.info("已添加video: {} .".format(rtsp_json['name']))
        return res

    @allure.step('api - 1. 添加PvgServer')
    def save_pvg_server(self, pvg_json, status='PASS'):
        api_url = "/api/video/save-pvg-server"
        method = 'POST'
        self.send_request(api_url, method, status, json=pvg_json)

        self.server_name = pvg_json['name']
        logger.info("已添加video: {} .".format(self.server_name))

    @allure.step('api - 2.1 查询VideoServer列表')
    def list_channel_tree_new(self, server_id=None, lv=0, page=1, status='PASS'):
        api_url = "/api/video/list-channel-tree-new"
        method = 'POST'
        data = {'type': 'Crowd', 'rows': 30}

        if server_id is not None:
            data['id'] = self.server_id
            data['lv'] = lv
            data['page'] = page

        res = self.send_request(api_url, method, status, data=data)

        logger.info("获取设备列表{} .".format(res))
        return res

    @allure.step('ext - 2. 获取ID')
    def get_serverid(self):
        channel_tree = self.list_channel_tree_new()
        # 获取指定video_name的设备ID
        ids = {}
        for kw in channel_tree.json():
            name = kw['name']
            ids[name] = kw['id']
        self.server_id = ids.get(self.server_name, None)
        logger.info("获取{}的ID为{}".format(self.server_name, self.server_id))

    @allure.step('ast - 3. 断言VideoServer资源数量')
    def assert_server_count(self, real_count):
        # 通过数据库确认camera数量
        query_camera_count = "SELECT COUNT(*) FROM t_video_channel " \
                             "WHERE F_Video_Server_ID = '{}' " \
                             "AND F_Enabled = 1;".format(self.server_id)
        # Sql().assert_query(query_camera_count, real_count)
        logger.info(query_camera_count)

        # 循环检查并断言camera数量
        init = -1
        start = datetime.datetime.now()
        while True:
            count = Sql().query(query_camera_count)[0][0]
            now = datetime.datetime.now()
            interval = (now - start).seconds
            if count == real_count:
                logger.info('查询完毕，数量匹配')
                res = 'SUCCESS'
                break
            elif count == init and interval > 30:
                logger.error('查询完毕，数量不匹配')
                res = 'FAIL'
                break
            else:
                init = count
                logger.info('查询中，已耗时{}，已同步{}条'.format((now - start), count))
                time.sleep(5)
        end = datetime.datetime.now()
        logger.info('总耗时:{}'.format(end - start))
        assert res == 'SUCCESS'

    @allure.step('api - 4. 同步PvgServer')
    def refresh_pvg_server(self, status='PASS'):
        api_url = "/api/video/refresh-pvg-server"
        method = 'POST'
        data = {'serverId': self.server_id}
        res = self.send_request(api_url, method, status, data=data)
        return res

    @allure.step('api - 4. 查询VideoServer详情')
    def video_server_detail(self, status='PASS'):
        api_url = "/api/video/video-server-detail"
        method = 'POST'
        data = {'videoServerId': self.server_id}
        res = self.send_request(api_url, method, status, data=data)
        return res

    @allure.step('api - 4. 查询VideoServer中任务开启数')
    def get_enable_task_count_by_videoserver(self, status='PASS'):
        api_url = "/api/task/get-enable-task-count-by-videoserver"
        method = 'POST'
        data = {'videoServerId': self.server_id}
        extractor = 'count'
        res = self.send_request(api_url, method, status, data=data, extractor=extractor)

        logger.info("该视频服务器下有{}个运行中的任务".format(res))
        return res

    @allure.step('api - 4. 重命名VideoServer')
    def update_server_name(self, rename, redescrip, version=None, status='PASS'):
        api_url = "/api/video/update-server-name"
        method = 'POST'
        data = {'serverId': self.server_id, 'serverName': rename, 'description': redescrip, 'version': version}
        res = self.send_request(api_url, method, status, data=data)
        return res

    @allure.step('api - 5. 删除VideoServer')
    def del_video_server(self, status='PASS'):
        api_url = "/api/video/del-video-server"
        method = 'POST'
        data = {'videoServerId': self.server_id, 'flag': 'true'}
        res = self.send_request(api_url, method, status, data=data)
        return res




