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
import time
import json
from testAPI.interface.inits.test_login import TestLogin
from utils.sql import Sql
import datetime

class TestAuth(unittest.TestCase):
    URL = Config().get('URL_CROWD', index=0)
    API_PATH = "/api/crowd-auth/set-auth-key"
    METHOD = 'POST'

    def setUp(self):
        headers = {'Authorization':
                        'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiO'
                        'iJhZG1pbiIsInJvbGUiOiJST0xFX1NV'
                        'UEVSX0FETUlOIiwiY3JlYXRlZCI6MTU0'
                        'NTY0NTU1MDQ5MywibmFtZSI6IiVFOCVCN'
                        'iU4NSVFNyVCQSVBNyVFNyVBRSVBMSVFNyU'
                        '5MCU4NiVFNSU5MSU5OCIsImV4cCI6MzYw'
                        'MDE1NDU2NDU1NTB9.5jaE90J0DO-Arp_a4'
                        'AyGeN4QOAH3pm5IC0OvKxawFfrxuXQpUROE7qildYsaHiI5t4RmdoI-4_n2dctLf9VBfg'}

        self.client = HTTPClient(url=self.URL + self.API_PATH, method=self.METHOD, headers=headers)

    def test_auth_set(self):
        license = {'license': open('172.17.3.34.license_key', 'rb')}
        # license = {'license': ('license_file', open('172.17.3.34.license_key', 'rb'), 'image/jpeg')}
        res = self.client.send(files=license)
        assertHTTPCode(res, [200])

    def tearDown(self):

        self.client.close()


if __name__ == '__main__':
    unittest.main()



