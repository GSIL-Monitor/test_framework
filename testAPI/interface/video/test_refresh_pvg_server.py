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


class TestRefreshPVG(unittest.TestCase):
    URL = Config().get('URL_CROWD', index=0)
    API_PATH0 = "/api/video/refresh-pvg-server"
    API_PATH1 = "/api/video/list-channel-tree-new"

    METHOD = 'POST'

    def setUp(self):
        headers = {'Authorization':
                       'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsInJv'
                       'bGUiOiJST0xFX1NVUEVSX0FETUlOIiwiY3JlYXRlZCI6MTU'
                       '0NDUwOTg4OTYzNCwibmFtZSI6IiVFOCVCNiU4NSVFNyVCQSV'
                       'BNyVFNyVBRSVBMSVFNyU5MCU4NiVFNSU5MSU5OCIsImV4cCI6M'
                       'zYwMDE1NDQ1MDk4ODl9.9MblG8SdAihA_n58S55X5Za57HycrOoS'
                       '4dHLx_1EhVp_Gk6-CHbzcNpSHEnuFYsX6FA3XBn_NyYZAboBtWZGhw'}

        self.client0 = HTTPClient(url=self.URL + self.API_PATH0, method=self.METHOD, headers=headers)
        self.client1 = HTTPClient(url=self.URL + self.API_PATH1, method=self.METHOD)

    def refresh_pvg_server(self, serverId, httpcode):
        data = { 'serverId': serverId }
        res = self.client0.send(data=data)
        assertHTTPCode(res, httpcode)
        return res

    def list_channel_tree_new(self, serverId, name, httpcode):
        data = {'type': 'Crowd', 'rows': 30, 'page': 1, 'lv': 0}
        data['id'] = serverId
        data['name'] = name
        res = self.client1.send(data=data)
        assertHTTPCode(res, httpcode)
        return res

    def tearDown(self):
        self.client0.close()
        self.client1.close()


if __name__ == '__main__':

    serverId = ['9D1CA771102A4F6E9C8A955C79137F9D', 'DD54F11273554A3BAF9DB9766ACF3B01']
    name = ['10.0.100.12', '10.0.100.36']

    test = TestRefreshPVG()
    test.setUp()
    res1 = test.refresh_pvg_server(serverId[0], [200])
    import time
    time.sleep(5)
    res2 = test.list_channel_tree_new(serverId[0], name[0], [200])
    res3 = test.list_channel_tree_new(serverId[1], name[1], [200])
    test.tearDown()
