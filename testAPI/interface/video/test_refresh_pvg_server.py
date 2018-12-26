# coding = utf-8
import os
import time
import unittest
from utils.config import Config, REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
from utils.support import encrypt
from utils.mail import Email
import time
import json
from testAPI.interface.inits.test_login import TestLogin
from utils.sql import Sql
import datetime


class TestRefreshPVG(unittest.TestCase):
    URL = Config().get('URL_CROWD', index=0)
    API_PATH0 = "/api/video/refresh-pvg-server"
    API_PATH1 = "/api/video/list-channel-tree-new"

    METHOD = 'POST'

    def setUp(self):
        headers = {'Authorization':
                       'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsInJv'
                       'bGUiOiJST0xFX1NVUEVSX0FETUlOIiwiY3JlYXRlZCI6MT'
                       'U0NTI3ODQ2MDc3MiwibmFtZSI6IiVFOCVCNiU4NSVFNyVC'
                       'QSVBNyVFNyVBRSVBMSVFNyU5MCU4NiVFNSU5MSU5OCIsImV'
                       '4cCI6MzYwMDE1NDUyNzg0NjB9.2iFcCMctryDuyv-YLYgfg'
                       'V9QbKBkET7oM44HPOOIdxMugZukOJbruOvLwZjVXpXlG_zsg'
                       'UCXIr23bBBNy-8jeQ'}

        self.client0 = HTTPClient(url=self.URL + self.API_PATH0, method=self.METHOD, headers=headers)
        self.client1 = HTTPClient(url=self.URL + self.API_PATH1, method=self.METHOD)

    @staticmethod
    def list_channel_tree(self, httpcode):
        data = {'type': 'Crowd', 'rows': 30}
        res = self.client1.send(data=data)
        assertHTTPCode(res, httpcode)
        return res

    def get_server_Id(self, video_ip):
        serverId = {}
        res = self.list_channel_tree(self, [200])
        for kw in res.json():
            name = kw['name']
            serverId[name] = kw['id']
        logger.info(serverId)
        return serverId[video_ip]

    def refresh_pvg_server(self, serverId, httpcode):
        data = {'serverId': serverId}
        res = self.client0.send(data=data)
        assertHTTPCode(res, httpcode)
        return res

    def list_channel_tree_new(self, serverId, name, httpcode):
        data = {'type': 'Crowd', 'rows': 30, 'page': 1, 'lv': 0}
        data['id'] = serverId
        data['name'] = name
        res = self.client1.send(data=data)
        assertHTTPCode(res, httpcode)
        return res

    def tearDown(self):
        self.client0.close()
        self.client1.close()


if __name__ == '__main__':

    test = TestRefreshPVG()
    test.setUp()

    name = '10.0.100.12'  # 是name，不是ipAddress
    real_count = 150
    Id = test.get_server_Id(name)
    res1 = test.refresh_pvg_server(Id, [200])

    query_camera_count = "SELECT COUNT(*) FROM t_video_channel " \
                         "WHERE F_Video_Server_ID = '{}' " \
                         "AND F_Enabled = 1;".format(Id)
    logger.info(query_camera_count)
    init = -1
    start = datetime.datetime.now()

    while True:
        count = Sql().query(query_camera_count)[0][0]
        now = datetime.datetime.now()
        interval = (now-start).seconds
        if count == real_count:
            logger.info('同步成功，数量匹配')
            break
        elif count == init and interval > 30:
            logger.error('同步失败，数量不匹配')
            break
        else:
            init = count
            logger.info('同步中，进行时间{}，已同步{}条'.format((now - start), count))
            time.sleep(5)

    end = datetime.datetime.now()
    logger.info('总耗时:{}'.format(end-start))

    test.tearDown()
