# coding = utf-8
import pytest
import allure
from testAPI.interface.conftest import auth_login, auth_logout


@allure.severity('block')
@allure.feature('设备状态')
@allure.story('设备信息')
def test_4301_server_info(user_env, user_success):
    my_user = user_env(user_success)
    my_user.get_server_info()

