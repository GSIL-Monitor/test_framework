# coding = utf-8
import pytest
import allure
from testAPI.interface.conftest import *


@allure.severity('blocker')
@allure.feature('登入登出')
@allure.story('登入')
@allure.title('登录成功')
@pytest.mark.parametrize('users', [admin, user])
def test_1101_login_success(users):
    """登陆成功"""
    auth_login(**users, status='PASS')


@allure.severity('blocker')
@allure.feature('登入登出')
@allure.story('登入')
@allure.title('登录失败')
@pytest.mark.parametrize('username', ['admin', 'user', '', ' ', 'ADMIN', 'Admin', 'True', '!~#$%*^&*()_+/&"`'])
@pytest.mark.parametrize('password', ['123456', '', '      ', '!~#$%*\\^&*()_+/&"`'])
def test_1102_login_fail(username, password):
    """使用错误密码登录失败"""
    res = auth_login(username, password, 'FAIL')
    assert 'Unauthorized' in res.text


if __name__ == '__main__':
    pytest.main(['test_11_login.py'])


