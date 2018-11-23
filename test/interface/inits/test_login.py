import os
import time
import unittest
from utils.config import Config, REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
from utils.support import encrypt


class TestLogin(unittest.TestCase):
    URL = Config().get('URL_CROWD', index=0)
    API_PATH = "/api/auth"
    METHOD = 'POST'

    def setUp(self):
        self.client = HTTPClient(url=self.URL+self.API_PATH, method=self.METHOD)

    def login(self, username, password, httpcode):
        auth_json = {"username": username, "password": encrypt(password)}
        res = self.client.send(json=auth_json)
        assertHTTPCode(res, httpcode)
        return res

    @unittest.skip("I don't want to run this case.")
    def test_login_success(self):
        """使用正确的用户名密码登录成功"""
        res1 = self.login('admin', 'ADMIN1', [200])
        self.assertIn('token', res1.text)
        return res1.json()['token']

    @unittest.skipIf(True, "I don't want to run this case.")
    def test_login_fail(self):
        """使用错误密码登录失败"""
        res2 = self.login('admin', 'admin1', [401, 405])
        self.assertNotIn('token', res2.text)

    def tearDown(self):
        self.client.close()


if __name__ == '__main__':
    REPORT_NAME = '{}-report.html'.format(time.strftime('%Y-%m-%d-%H-%M-%S'))
    report = os.path.join(REPORT_PATH, REPORT_NAME)

    suite = unittest.TestSuite()
    tests = [TestLogin('test_login_success'), TestLogin('test_login_fail')]
    suite.addTests(tests)
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='测试框架', description='接口html报告')
        runner.run(suite)