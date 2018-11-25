import os
import time
import unittest
from utils.config import Config, REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
from utils.mail import Email


class TestBaiDuHTTP(unittest.TestCase):
    URL = Config().get('URL')

    def setUp(self):
        self.client = HTTPClient(url=self.URL, method='GET')

    def test_baidu_http(self):
        res = self.client.send()
        logger.debug(res.text)
        assertHTTPCode(res, [200])
        self.assertIn('百度一下，你就知道', res.text)


if __name__ == '__main__':

    REPORT_NAME = '{}-report.html'.format(time.strftime('%Y-%m-%d-%H-%M-%S'))
    report = os.path.join(REPORT_PATH, REPORT_NAME)

    with open(report, 'wb') as rp:
        runner = HTMLTestRunner(rp, verbosity=2, title='测试框架', description='接口html报告')
        runner.run(TestBaiDuHTTP('test_baidu_http'))

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
