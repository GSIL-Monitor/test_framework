# coding = utf-8
import os
import time
import unittest
from utils.config import Config, REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
from utils.support import encrypt
from utils.mail import Email


class TestListChannel(unittest.TestCase):
    URL = Config().get('URL_CROWD', index=0)
    API_PATH0 = "/api/video/save-pvg-server"
    API_PATH1 = "/api/video/init-channel-tree"
    API_PATH1 = "/api/video/list-channel-tree-new"

    METHOD = 'POST'

    def setUp(self):
        self.client0 = HTTPClient(url=self.URL + self.API_PATH0, method=self.METHOD)
        self.client1 = HTTPClient(url=self.URL + self.API_PATH1, method=self.METHOD)
        self.client2 = HTTPClient(url=self.URL + self.API_PATH2, method=self.METHOD)

    def save_pvg_server(self, httpcode):
        pass

    def init_channel_tree(self, httpcode):
        pass

    def list_channel_tree_new(self, httpcode):
        pass

    def tearDown(self):
        self.client0.close()
        self.client1.close()
        self.client2.close()


if __name__ == '__main__':
    REPORT_NAME = '{}-report.html'.format(time.strftime('%Y-%m-%d-%H-%M-%S'))
    report = os.path.join(REPORT_PATH, REPORT_NAME)

    suite = unittest.TestSuite()
    tests = [TestLogin('test_login_success'), TestLogin('test_login_fail')]
    suite.addTests(tests)
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='测试框架', description='接口html报告')
        runner.run(suite)

    _email = Config().get('email')

    message1 = '这是今天的测试报告'
    message2 = open(report, 'r', encoding='utf-8').read()

    e = Email(title=_email.get('title'),
              receiver=_email.get('receiver'),
              server=_email.get('server'),
              sender=_email.get('sender'),
              password=_email.get('password'),
              path=report,
              message='{0}\n{1}'.format(message1, message2)
              )
    e.send()
