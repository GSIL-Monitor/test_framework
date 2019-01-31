# coding = utf-8
import pytest
import allure
from utils.config import Config
from utils.support import encrypt
from testAPI.common.pre_request import PRequest
from testAPI.interface.mod_2_video.conftest import video_env
from testAPI.interface.mod_3_task.conftest import task_env
from testAPI.interface.mod_4_user.conftest import user_env

__all__ = (
    'base_url',
    'auth_login',
    'auth_logout',
    'admin',
    'user',
    'video_env',
    'task_env',
    'user_env'
)

base_url = Config().get('BASE_URL', index=0)
config_user = Config('apiuser.yml')
admin = config_user.get('admin')
user = config_user.get('user')


@allure.step('api - 登入')
def auth_login(username, password, status='PASS'):
    """登录并获取token"""
    api_url = "/api/auth"
    method = 'POST'
    JSON = {"username": username, "password": encrypt(password)}
    extractor = 'token'
    token = PRequest().send_request(api_url, method, status, json=JSON, extractor=extractor)
    return token


@allure.step('api - 登出')
def auth_logout(token, status='PASS'):
    """登录并获取token"""
    api_url = "/api/log/log-out"
    method = 'POST'
    token = PRequest(token).send_request(api_url, method, status)
    return token


@pytest.fixture(scope='session')
def login_admin():
    token = auth_login(**admin)
    yield token
    auth_logout(token)


@pytest.fixture(scope='session')
def login_user():
    token = auth_login(**user)
    yield token
    auth_logout(token)
