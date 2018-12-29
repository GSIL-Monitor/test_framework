# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言

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
import pytest
import allure_pytest
from utils.extractor import JMESPathExtractor
import allure
import datetime
from utils.sql import Sql
from injson import check
from json import JSONEncoder

__all__ = ('base_url',
           'json_pvg',
           'save_pvg_server',
           'list_channel_tree_new',
           'assert_server_count',
           'refresh_pvg_server',
           'video_server_detail',
           'get_enable_task_count_by_videoserver',
           'del_video_server',
           'update_server_name'
           )

base_url = Config().get('BASE_URL', index=0)

dicts_pvg_67 = Config().get('pvg_server_67', index=1)
real_count_67 = dicts_pvg_67.pop('real_count')
json_pvg_67 = JSONEncoder().encode(dicts_pvg_67)

dicts_pvg_10 = Config().get('pvg_server_10', index=0)
real_count_10 = dicts_pvg_10.pop('real_count')
json_pvg_10 = JSONEncoder().encode(dicts_pvg_10)

json_pvg = [(dicts_pvg_67, real_count_67, [200])]
# json_pvg = [(json_pvg_67, real_count_67, [200]), (json_pvg_10, real_count_10, [200])]


@pytest.fixture(scope='module', params=json_pvg)
def init_pvg_server(login_admin, request):
    json, real_count, httpcode = request.param

    save_pvg_server(login_admin, json, httpcode)
    server_id = list_channel_tree_new(json['name'], httpcode)
    assert_server_count(server_id, real_count)
    res = video_server_detail(login_admin, server_id, httpcode)
    check(json, res.json())
    yield res.json()
    del_video_server(login_admin, server_id, httpcode)


@allure.step('api - 添加VideoServer')
def save_pvg_server(login_admin, json, httpcode):

    api_url = "/api/video/save-pvg-server"
    method = 'POST'

    headers = {'Authorization': login_admin}
    client = HTTPClient(url=(base_url+api_url), method=method, headers=headers)
    res = client.send(json=json)
    assert res.status_code in httpcode

    return res


@allure.step('api - 查询VideoServer列表, ext - 获取{video_name}的ID')
def list_channel_tree_new(video_name, httpcode):
    api_url = "/api/video/list-channel-tree-new"
    method = 'POST'
    data = {'type': 'Crowd', 'rows': 30}

    client = HTTPClient(url=(base_url+api_url), method=method)
    res = client.send(data=data)
    assert res.status_code in httpcode

    server_id = {}
    for kw in res.json():
        name = kw['name']
        server_id[name] = kw['id']
    return server_id[video_name]


@allure.step('api - 同步PvgServer')
def refresh_pvg_server(login_admin, server_id, httpcode):
    api_url = "/api/video/refresh-pvg-server"
    method = 'POST'
    data = {'serverId': server_id}

    headers = {'Authorization': login_admin}
    client = HTTPClient(url=(base_url+api_url), method=method, headers=headers)
    res = client.send(data=data)

    assert res.status_code in httpcode
    return res


@allure.step('ast - 断言VideoServer资源数量')
def assert_server_count(server_id, real_count):
    query_camera_count = "SELECT COUNT(*) FROM t_video_channel " \
                         "WHERE F_Video_Server_ID = '{}' " \
                         "AND F_Enabled = 1;".format(server_id)
    logger.info(query_camera_count)
    init = -1
    start = datetime.datetime.now()

    while True:
        count = Sql().query(query_camera_count)[0][0]
        now = datetime.datetime.now()
        interval = (now - start).seconds
        if count == real_count:
            logger.info('同步成功，数量匹配')
            res = 'SUCCESS'
            break
        elif count == init and interval > 30:
            logger.error('同步失败，数量不匹配')
            res = 'FAIL'
            break
        else:
            init = count
            logger.info('同步中，进行时间{}，已同步{}条'.format((now - start), count))
            time.sleep(5)

    end = datetime.datetime.now()
    logger.info('总耗时:{}'.format(end - start))
    assert res == 'SUCCESS'


@allure.step('api - 查询VideoServer详情')
def video_server_detail(login_admin, server_id, httpcode):
    api_url = "/api/video/video-server-detail"
    method = 'POST'
    data = {'videoServerId': server_id}

    headers = {'Authorization': login_admin}
    client = HTTPClient(url=(base_url+api_url), method=method, headers=headers)
    res = client.send(data=data)

    assert res.status_code in httpcode
    return res


@allure.step('api - 查询VideoServer中任务开启数')
def get_enable_task_count_by_videoserver(login_admin, server_id, httpcode):
    api_url = "/api/task/get-enable-task-count-by-videoserver"
    method = 'POST'
    data = {'serverId': server_id}
    extractor = 'count'

    headers = {'Authorization': login_admin}
    client = HTTPClient(url=(base_url+api_url), method=method, headers=headers)
    res = client.send(data=data)

    assert res.status_code in httpcode
    res = JMESPathExtractor().extract(extractor, res.text) if extractor else res
    return res


@allure.step('api - 删除VideoServer')
def del_video_server(login_admin, server_id, httpcode):
    api_url = "/api/video/del-video-server"
    method = 'POST'
    data = {'videoServerId': server_id, 'flag': 'true'}

    headers = {'Authorization': login_admin}
    client = HTTPClient(url=(base_url+api_url), method=method, headers=headers)
    res = client.send(data=data)

    assert res.status_code in httpcode
    return res


@allure.step('api - 重命名VideoServer')
def update_server_name(login_admin, server_id, server_name, description, version, httpcode):
    api_url = "/api/video/update-server-name"
    method = 'POST'
    data = {'serverId': server_id, 'serverName': server_name, 'description': description, 'version': version}

    headers = {'Authorization': login_admin}
    client = HTTPClient(url=(base_url+api_url), method=method, headers=headers)
    res = client.send(data=data)

    assert res.status_code in httpcode
    return res

