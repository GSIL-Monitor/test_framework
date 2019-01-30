# coding = utf-8
"""
api-接口请求， ext-结果提取处理， ast-自定义断言
"""
import os
import pytest
import allure
from utils.config import Config, DATA_PATH
from testAPI.common.pre_request import PRequest


__all__ = (
    'base_url',
    'license_right',
    'license_wrong',
    'hard_info',
    'APIAuth'
)

base_url = Config().get('BASE_URL', index=0)
hard_info = '{}.hardinfo'.format(base_url.partition("://")[-1])
license_right = '{}.license_key'.format(base_url.partition("://")[-1])
license_wrong = 'error.license_key'


@pytest.fixture()
def auth_api(login_admin):
    auth = APIAuth(login_admin)
    yield auth


class APIAuth(PRequest):
    """
    登录授权类
    """

    def __init__(self, login):
        """
        1. 继承父类构造函数，获取登录token，传递给自定义接口请求函数self.send_request
        2. 初始化类属性
        """
        super(APIAuth, self).__init__(login)

    @allure.step('api - 获取硬件信息')
    def get_hard_ware_info(self, status='PASS'):
        api_url = "/api/crowd-auth/get-hard-ware-info"
        method = 'POST'
        res = self.send_request(api_url, method, status)
        return res

    @allure.step('api - 导入授权')
    def set_auth_key(self, license, status='PASS'):
        api_url = "/api/crowd-auth/set-auth-key"
        method = 'POST'
        license_file = os.path.join(DATA_PATH, 'license', license)
        res = self.send_request(api_url, method, status, files={'license': open(license_file, 'rb')})
        return res

    @allure.step('api - 获取授权状态')
    def get_auth_info(self, status='PASS'):
        api_url = "/api/crowd-auth/get-auth-info"
        method = 'POST'
        extractor = 'ext'
        res = self.send_request(api_url, method, status, extractor=extractor)
        return res

    @allure.step('api - 文件导出')
    def export_file(self, req_name='hardwares.zip', file_path='data/ex_auth/hardwares_test.zip'):
        api_url = "/export/{}".format(req_name)
        method = 'GET'
        res = self.send_request(api_url, method)

        abs_exp_file = Config(file_path).file
        with open(abs_exp_file, "wb") as exp:
            exp.write(res.content)
        assert os.path.getsize(abs_exp_file)
        return abs_exp_file
