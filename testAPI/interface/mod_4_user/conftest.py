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
# from testAPI.interface.mod_2_video.conftest import video_env
# from testAPI.interface.mod_3_task.conftest import task_env


__all__ = (
    'APIUser'
)

config_user = Config('apiuser.yml')


@pytest.fixture()
def user_api(task_env):
    my_user = APIUser()

    def parse_api_user(user_conf):
        my_user.parse_conf_user(task_env, user_conf)
        return my_user
    yield parse_api_user
    my_user.delete_user()
    my_user.assert_user_attr('FAIL')


@pytest.fixture(scope='session')
def user_env(task_env):
    my_user = APIUser()
    load_user_data()

    def parse_env_user(user_conf):
        my_user.parse_conf_user(task_env, user_conf)
        my_user.id = my_user.get_user_attr("id")
        return my_user
    yield parse_env_user


class APIUser(PRequest):
    """
    用户接口类
    """

    def __init__(self, login=None):
        # 初始化入参
        super(APIUser, self).__init__(login)
        # 初始化类属性
        self.user_conf = None
        self.id = None
        self.user = None
        self.password = None
        self.channel_name_list = None

    @allure.step('ext - 0. 预处理数据，获取待添加用户的设备ID')
    def parse_conf_user(self, parse_env_task, user_conf):
        self.user_conf = config_user.get(user_conf)
        self.user = self.user_conf["userId"]
        self.password = self.user_conf["password"]
        self.user_conf["password"] = encrypt(self.user_conf["password"])

        channel_id_list = []
        channel_name_list = []
        for channel_conf in self.user_conf.get('cameraNames'):
            _task_obj = parse_env_task(channel_conf)
            channel_id_list.append(_task_obj.channelId)
            channel_name_list.append(_task_obj.tasks_conf["channelName"])
            self.login = _task_obj.login

        self.user_conf["cameraIds"] = json.dumps(channel_id_list)
        self.channel_name_list = channel_name_list
        logger.debug('获取用户 "{}" 待添加设备IDs: {} '.format(self.user, self.user_conf["cameraIds"]))
        return

    @allure.step('api - 1. 添加用户')
    def add_user(self, status='PASS'):
        api_url = "/api/user/add-user"
        method = 'POST'
        data = self.user_conf
        self.send_request(api_url, method, status, data=data)
        self.id = self.get_user_attr("id")
        assert self.id is not None

    @allure.step('ext - 2.1. 获取用户属性')
    def get_user_attr(self, *user_attr):
        """
        每次用户更新都要执行这句话：增加、修改、删除
        根据唯一账户名，获得对应用户的后台ID、角色、名称
        >>>self.get_user_attr("id")
        >>>self.get_user_attr("uname")
        >>>self.get_user_attr("roleType")
        >>>self.get_user_attr("id", "uname", "roleType")
        """
        users_list_json = self.list_user()
        for usr in users_list_json.get('rows'):
            if usr.get('uid') == self.user_conf['userId']:
                val = [usr.get(attr) for attr in user_attr]
                logger.debug('获取用户{}属性: {} = {} '.format(self.user, user_attr, val))
                return val[0] if len(val) == 1 else val
        val = [None for attr in user_attr]
        return val[0] if len(val) == 1 else val

    @allure.step('ast - 2.2. 断言用户信息符合预期')
    def assert_user_attr(self, status='PASS'):
        self.id, name, role = self.get_user_attr("id", "uname", "roleType")
        if status == 'FAIL' and not self.id:
            logger.info('用户{}不存在, 断言成功'.format(self.user_conf.get('userId')))
        elif status == 'PASS' and self.id:
            assert name == self.user_conf.get('userName')
            assert role == self.user_conf.get('roleType')
            logger.info('用户{}存在, 且信息匹配，断言成功'.format(self.user_conf.get('userId')))
        else:
            raise AttributeError('用户信息不匹配，断言失败')

    @allure.step('api - 3.1 获取用户名称列表')
    def list_user_id_name(self, status='PASS'):
        api_url = "/api/user/list-user-id-name"
        method = 'GET'
        res = self.send_request(api_url, method, status)
        users = [user["name"] for user in res.json()]
        logger.info(users)

    @allure.step('api - 3.2 获取用户概要信息列表')
    def list_user(self, status='PASS'):
        api_url = "/api/user/list-user"
        method = 'POST'
        data = {'page': 1, 'rows': 20, 'sidx': 'uid', 'sord': 'asc', 'searchString': '{"roleType":"","name":""}'}
        res = self.send_request(api_url, method, status, data=data)
        return res.json()

    @allure.step('api - 3.3 获取指定用户的详细信息')
    def user_detail(self, status='PASS'):
        api_url = "/api/user/user-detail"
        method = 'POST'
        data = {'id': self.id}
        res = self.send_request(api_url, method, status, data=data, extractor='cameraRole')
        return res

    @allure.step('ast - 3.4 断言用户相机权限分配符合预期')
    def assert_cameras(self):
        camera_role = self.user_detail()
        camera_list = [i.get('channelName') for i in camera_role if camera_role]
        assert set(camera_list) == set(self.channel_name_list)
        logger.info('用户相机列表分配，断言成功')

    @allure.step('api - 4. 修改用户信息')
    def update_user(self, status='PASS'):
        api_url = "/api/user/update-user"
        method = 'POST'
        data = {'id': self.id, **self.user_conf}
        data.pop('userId')
        res = self.send_request(api_url, method, status, data=data)

    @allure.step('api - 5. 删除用户')
    def delete_user(self, status='PASS'):
        api_url = "/api/user/delete-user"
        method = 'POST'
        data = {'id': self.id}
        res = self.send_request(api_url, method, status, data=data)

    @allure.step('api - 6. 重置密码')
    def reset_pwd(self, newPwd, status='PASS'):
        api_url = "/api/user/reset-pwd"
        method = 'POST'
        data = {'oldPwd': self.user_conf["password"], 'newPwd': newPwd}
        res = self.send_request(api_url, method, status, data=data)
        return res


