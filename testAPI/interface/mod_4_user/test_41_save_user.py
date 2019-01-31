# coding = utf-8
import pytest
import allure
from testAPI.interface.conftest import *


@allure.severity('block')
@allure.feature('用户管理')
@allure.story('添加正确的用户')
@pytest.mark.parametrize('user_success', ['user_one', 'user_two'])
def test_4101_add_user(user_api, user_success):
    my_user = user_api(user_success)
    my_user.add_user()
    my_user.assert_user_attr()
    my_user.assert_cameras()
    token = auth_login(my_user.user, my_user.password)
    auth_logout(token)

