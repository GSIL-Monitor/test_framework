# coding = utf-8
import os
import time
import pytest
import allure
from utils.support import unzip
from .conftest import *


@allure.severity('blocker')
@allure.feature('授权管理')
@allure.story('导入授权')
@allure.title('授权导入失败')
def test_1201_set_auth_wrong(auth_api):
    """授权导入测试"""
    auth_api.set_auth_key(license_wrong)
    time.sleep(3)
    res = auth_api.get_auth_info()
    assert res == '0'


@allure.severity('blocker')
@allure.feature('授权管理')
@allure.story('导入授权')
@allure.title('授权导入成功')
def test_1202_set_auth_right(auth_api):
    """授权导入测试"""
    auth_api.set_auth_key(license_right)
    time.sleep(3)
    res = auth_api.get_auth_info()
    assert res == '16'


@allure.severity('blocker')
@allure.feature('授权管理')
@allure.story('获取硬件信息')
def test_1203_get_auth_key(auth_api):
    """硬件信息"""
    auth_api.get_hard_ware_info()
    abs_exp_file = auth_api.export_file()
    unzip(abs_exp_file, os.path.dirname(abs_exp_file))
    abs_hard_info = os.path.join(os.path.dirname(abs_exp_file), hard_info)
    assert os.path.getsize(abs_hard_info)
    os.remove(abs_hard_info)




