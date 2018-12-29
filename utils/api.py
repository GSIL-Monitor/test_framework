# encoding: utf-8

import os
import unittest

from utils import (log, extractor, config, file_reader, client, assertion,
                   support, generator, HTMLTestRunner, funny)


class TestLeader(object):

    def __init__(self, **kwargs):
        """initialize TestLeader.

        :param kwargs:
        """
        self.unittest_runner = unittest.TextTestRunner(**kwargs)
        self.test_loader = unittest.TestLoader()
        self.summary = None





# if __name__ == '__main__':
#     REPORT_NAME = '{}-report.html'.format(time.strftime('%Y-%m-%d-%H-%M-%S'))
#     report = os.path.join(REPORT_PATH, REPORT_NAME)
#
#     suite = unittest.TestSuite()
#     tests = [TestLogin('test_login_success'), TestLogin('test_login_fail')]
#     suite.addTests(tests)
#     with open(report, 'wb') as f:
#         runner = HTMLTestRunner(f, verbosity=2, title='测试框架', description='接口html报告')
#         runner.run(suite)
#
#     _email = Config().get('email')
#
#     message1 = '这是今天的测试报告'
#     message2 = open(report, 'r', encoding='utf-8').read()
#
#     e = Email(title=_email.get('title'),
#               receiver=_email.get('receiver'),
#               server=_email.get('server'),
#               sender=_email.get('sender'),
#               password=_email.get('password'),
#               path=report,
#               message='{0}\n{1}'.format(message1, message2)
#               )
#     e.send()
#
