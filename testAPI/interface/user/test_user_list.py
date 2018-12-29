import sys
import time
import unittest
from utils.config import Config
from utils.client import HTTPClient
from utils.assertion import assertHTTPCode
from utils.support import encrypt


class TestUserList(unittest.TestCase):
    URL = Config().get('BASE_URL', index=0)
    API_PATH = "/api/user/list-user-id-name"
    METHOD = 'GET'

    def setUp(self):
        #headers={'Authorization': ''}
        self.client = HTTPClient(url=self.URL+self.API_PATH, method=self.METHOD)

    def user_list_id_name(self, username, password, httpcode):
        auth_json = {"username": username, "password": encrypt(password)}
        res = self.client.send(json=auth_json)
        assertHTTPCode(res, httpcode)
        return res

    @unittest.skip("I don't want to run this case.")
    def test_user_list_id_name(self):
        """"""
        pass

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

