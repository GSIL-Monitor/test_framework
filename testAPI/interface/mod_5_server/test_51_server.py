# coding = utf-8
import pytest
import allure
import json
from injson import check
from testAPI.interface.conftest import auth_login, auth_logout
from utils.log import logger
from utils.config import Config


@allure.severity('block')
@allure.feature('设备状态')
@allure.story('设备信息')
def test_4301_server_info(server_env):
    try:
        server_info = server_env.get_server_info()
        server_json = Config('testAPI/interface/mod_5_server/server.json').json()
        assert check(server_json, server_info)
    except Exception as e:
        raise e

