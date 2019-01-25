# coding = utf-8

import os
import unittest
from utils.config import Config, REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.extractor import JMESPathExtractor

base_url = Config().get('BASE_URL', index=0)


class PRequest(object):

    def __init__(self, login=None):
        self.login = login

    def send_request(self, api_url, method='POST', status='PASS', params=None, data=None, json=None, files=None, extractor=None):
        """请求定制封装"""
        # 登录，获取请求头的值
        headers = {'Authorization': self.login} if self.login else None

        # 建立http连接，发送请求
        client = HTTPClient(url=(base_url + api_url), method=method, headers=headers)
        response = client.send(params=params, json=json, data=data, files=files)
        try:
            # 有效用例和无效用例的最基本断言（针对status_code）
            if status == 'PASS':
                assert response.status_code in [200]
            elif status == 'FAIL':
                assert response.status_code not in [200]

            # 提取json值
            if status == 'PASS' and extractor is not None:
                response = JMESPathExtractor().extract(extractor, response.text)
                logger.info("数据处理: 提取{}的值为{} ".format(extractor, response))
        except Exception as e:
            logger.error(e)
        client.close()
        return response

