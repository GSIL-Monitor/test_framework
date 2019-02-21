# coding = utf-8
import pytest
import allure
from testAPI.interface.conftest import auth_login, auth_logout


@allure.severity('critical')
@allure.feature('用户管理')
@allure.story('修改用户名')
@pytest.mark.parametrize('user_success', ['user_one', 'user_two'])
def test_4201_update_user_name(user_env, user_success):
    my_user = user_env(user_success)
    my_user.user_conf['userName'] = '张三大爷'
    my_user.update_user()
    my_user.assert_user_attr()


@allure.severity('critical')
@allure.feature('用户管理')
@allure.story('修改用户角色')
@pytest.mark.parametrize('user_success', ['user_one', 'user_two'])
def test_4202_update_user_role(user_env, user_success):
    my_user = user_env(user_success)
    my_user.role = my_user.user_conf['roleType']
    my_user.user_conf['roleType'] = "ROLE_ADMIN"
    my_user.update_user()
    my_user.assert_user_attr()
    my_user.user_conf['roleType'] = my_user.role
    my_user.update_user()
    my_user.assert_user_attr()


# @allure.severity('block')
# @allure.feature('用户管理')
# @allure.story('重置密码')
# def test_4203_reset_passwd(user_env):
#     my_user = user_env('user_one')
#     my_user.update_user()
#     my_user.assert_user_attr()

