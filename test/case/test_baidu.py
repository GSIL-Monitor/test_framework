# -*- coding: utf-8 -*-
import os
import time
import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
from utils.config import Config, DRIVERS_PATH, DATA_PATH, REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.mail import Email
from test.page.baidu_result_page import BaiDuMainPage, BaiDuResultPage


class TestBaiDu(unittest.TestCase):
    URL = Config().get('URL')
    excel = os.path.join(DATA_PATH, 'test.xlsx')
    # driver_path = os.path.join(DRIVERS_PATH, 'chromedriver.exe')
    #
    # locator_kw = (By.ID, 'kw')
    # locator_su = (By.ID, 'su')
    # locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    def sub_setUp(self):
        # self.driver = webdriver.Chrome(executable_path=self.driver_path)
        # self.driver.get(self.URL)
        self.page = BaiDuMainPage(browser_type='chrome').get(self.URL, maximize_window=False)

    def sub_tearDown(self):
        # self.driver.quit()
        self.page.quit()

    def test_search(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            with self.subTest(data=d):
                self.sub_setUp()
                # self.driver.find_element(*self.locator_kw).send_keys(d['search'])
                # self.driver.find_element(*self.locator_su).click()
                self.page.search(d['search'])
                time.sleep(3)
                # links = self.driver.find_elements(*self.locator_result)
                self.page = BaiDuResultPage(self.page)  # 页面跳转到result page
                links = self.page.result_links
                for link in links:
                    logger.info(link.text)
                self.sub_tearDown()


if __name__ == '__main__':
    # unittest.main(verbosity=2)
    report = os.path.join(REPORT_PATH, 'report.html')
    with open(report, 'wb') as rp:
        runner = HTMLTestRunner(rp, verbosity=2, title='测试框架练习', description='生成html报告')
        runner.run(TestBaiDu('test_search'))

    e = Email(title='搜索功能测试报告',
              message='这是今天的测试报告，请查收！',
              receiver='zhangjiukun@sensenets.com',
              server='smtp.exmail.qq.com:465',
              sender='zhangjiukun@sensenets.com',
              password='Sensenets1992',
              path=report
              )
    e.send()

