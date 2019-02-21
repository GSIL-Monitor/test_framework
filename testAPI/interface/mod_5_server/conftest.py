# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言
import json
import pytest
import allure
from utils.config import Config
from utils.log import logger
from utils.sql import Sql
from utils.support import encrypt
from testAPI.common.pre_request import PRequest
from testAPI.common.pre_sql_data import *
from testAPI.interface import conftest


__all__ = (
    'APIServer'
)


@pytest.fixture(scope='session')
def server_env(login_admin, video_env):
    my_server = APIServer(login_admin)
    return my_server


class APIServer(PRequest):
    """
    用户接口类
    """

    def __init__(self, login=None):
        # 初始化入参
        super(APIServer, self).__init__(login)
        # 初始化类属性

    @allure.step('api - 1. 设备状态')
    def get_server_info(self, status='PASS'):
        api_url = "/api/server/get-server-info"
        method = 'POST'
        res = self.send_request(api_url, method, status)
        logger.debug(res.json())
        return res.json()


