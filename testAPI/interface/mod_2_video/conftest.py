# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言
import pytest
import allure
import time
import datetime
from utils.config import Config
from utils.log import logger
from utils.sql import Sql
from testAPI.common.pre_request import PRequest
from testAPI.common.pre_sql_data import *


__all__ = (
    'APIVideo',
    'video_env'
)


config_video = Config('apivideo.yml')


@pytest.fixture()
def video_api(login_admin):
    """
    1)增删改查中的‘增删’，需要干净的环境; 2)固件执行范围为function级别
    """
    av = APIVideo(login_admin)
    yield av
    if av.video_conf.get('version') == 'rtsp':
        av.del_rtsp_video()
    else:
        av.del_video_server()
    assert av.query_video_id(av.video_conf) is None


@pytest.fixture(scope='module')
def video_env(login_admin):
    """
    1)增删改查中的‘改查’ , 预先准备所需‘数据环境’; 2)固件执行范围为module级别
    """
    env_video = APIVideo(login_admin)
    load_video_data()

    def parse_env_video(video_server_conf, index=0):
        env_video.video_conf = config_video.get(video_server_conf, index)
        env_video.server_id = env_video.query_video_id(env_video.video_conf)
        return env_video
    yield parse_env_video
    # clear_all()


class APIVideo(PRequest):
    """
    视频接口类
    """

    def __init__(self, login=None):
        """
        1. 继承父类构造函数，获取登录token，传递给自定义接口请求函数self.send_request
        2. 初始化类属性（名称、ID、子设备数）
        """
        super(APIVideo, self).__init__(login)
        self.video_conf = None
        self.server_id = None

    @allure.step('ext - 0. 添加视频 <添加pvg/rtsp视频> ')
    def save_video(self, video_server, index=0, status='PASS'):
        # 初始化视频服务配置 self.video_conf, 断言并获取全局唯一ID self.server_id，
        self.video_conf = config_video.get(video_server, index)
        if self.video_conf.get('version') == 'rtsp':
            self.save_rtsp(self.video_conf, status)
        else:
            self.save_pvg_server(self.video_conf, status)
        # yml文件以'---'分割，第一章节(index==0)为有效用例(断言成功），后续章节(index!=0)为无效用例（断言失败）
        self.server_id = self.query_video_id(self.video_conf)
        assert self.server_id is None if index else self.server_id is not None

    @allure.step('api - 1. 添加rtsp视频')
    def save_rtsp(self, rtsp_json, status='PASS'):
        api_url = "/api/video/save-rtsp"
        method = 'POST'
        data = {'rtspUrl': rtsp_json['url'], 'rtspName': rtsp_json['name']}
        self.send_request(api_url, method, status, data=data)

    @allure.step('api - 1. 添加PvgServer')
    def save_pvg_server(self, pvg_json, status='PASS'):
        api_url = "/api/video/save-pvg-server"
        method = 'POST'
        self.send_request(api_url, method, status, json=pvg_json)

    @staticmethod
    @allure.step('ext - 1. 获取视频服务ID ')
    def query_video_id(video_conf):
        mysql = Sql()
        if video_conf['version'] == 'rtsp':
            sql_video_id = "SELECT F_ID FROM t_video_channel WHERE F_Name = '{}' AND " \
                           "F_Video_Type = 'rtsp' AND  F_Enabled = 1;".format(video_conf['name'])
        else:
            sql_video_id = "SELECT F_ID FROM t_video_server WHERE F_NAME = '{}' AND " \
                           "F_Video_Type = 'pvg' AND F_Enabled = 1;".format(video_conf['name'])
        req = mysql.query(sql_video_id)
        mysql.close()
        server_id = req[0][0] if req else None
        logger.debug('获取 {} ID: {}'.format(video_conf['name'], server_id))
        return server_id

    @allure.step('ast - 1. 断言VideoServer资源数量')
    def assert_server_count(self):
        # 通过数据库确认camera数量
        query_camera_count = "SELECT COUNT(*) FROM t_video_channel " \
                             "WHERE F_Video_Server_ID = '{}' " \
                             "AND F_Enabled = 1;".format(self.server_id)
        # logger.debug(query_camera_count)

        # 循环检查并断言camera数量
        init = -1
        start = datetime.datetime.now()
        while True:
            count = Sql().query(query_camera_count)[0][0]
            now = datetime.datetime.now()
            interval = (now - start).seconds
            if count == self.video_conf['real_count']:
                logger.info('查询完毕，结果{}匹配'.format(count))
                res = 'SUCCESS'
                break
            elif count == init and interval > 30:
                logger.error('查询完毕，结果不匹配')
                res = 'FAIL'
                break
            else:
                init = count
                logger.info('查询中，已耗时{}，已同步{}条'.format((now - start), count))
                time.sleep(5)
        end = datetime.datetime.now()
        logger.info('总耗时:{}'.format(end - start))
        assert res == 'SUCCESS'

    @allure.step('api - 2. 同步PvgServer')
    def refresh_pvg_server(self, status='PASS'):
        api_url = "/api/video/refresh-pvg-server"
        method = 'POST'
        data = {'serverId': self.server_id}
        res = self.send_request(api_url, method, status, data=data)
        return res

    @allure.step('api - 3 查询VideoServer列表')
    def list_channel_tree_new(self, server_id=None, lv=0, page=1, status='PASS'):
        api_url = "/api/video/list-channel-tree-new"
        method = 'POST'
        data = {'type': 'Crowd', 'rows': 30}

        if server_id is not None:
            data['id'] = self.server_id
            data['lv'] = lv
            data['page'] = page
        res = self.send_request(api_url, method, status, data=data)
        logger.debug("获取设备列表{} .".format(res))
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
        logger.debug("该视频服务器下有{}个运行中的任务".format(res))
        return res

    @allure.step('api - 5. 重命名VideoServer')
    def update_server_name(self, rename, redescrip, version=None, status='PASS'):
        api_url = "/api/video/update-server-name"
        method = 'POST'
        data = {'serverId': self.server_id, 'serverName': rename, 'description': redescrip, 'version': version}
        res = self.send_request(api_url, method, status, data=data)
        return res

    @allure.step('api - 6. 删除VideoServer')
    def del_video_server(self, status='PASS'):
        api_url = "/api/video/del-video-server"
        method = 'POST'
        data = {'videoServerId': self.server_id, 'flag': 'true'}
        res = self.send_request(api_url, method, status, data=data)
        return res

    @allure.step('api - 6. 删除RtspVideo')
    def del_rtsp_video(self, status='PASS'):
        api_url = "/api/video/del-rtsp-video"
        method = 'POST'
        data = {'channelId': self.server_id, 'taskType': 'Crowd', 'flag': 'false'}
        res = self.send_request(api_url, method, status, data=data)
        return res

