# coding = utf-8
import pytest
import allure
from datetime import datetime, timedelta
from testAPI.interface.conftest import auth_login, auth_logout


@allure.severity('critical')
@allure.feature('状态监测')
@allure.story('获取实时分组状态')
def test_6101_real_status_groups(status_api):
    try:
        my_status = status_api('crowd_channel_1')
        res = my_status.status_group()
        assert res.get('rows')
    except Exception as e:
        raise e


@allure.severity('critical')
@allure.feature('状态监测')
@allure.story('获取实时任务状态')
def test_6102_real_status_tasks(status_api):
    try:
        my_status = status_api('crowd_channel_1', 'crowd_channel_2', 'crowd_channel_3', 'crowd_channel_4', 'crowd_channel_5', 'crowd_channel_6')
        res = my_status.status_channel()
        assert res.get('additional').get('allPeopleCount')
    except Exception as e:
        raise e


@allure.severity('critical')
@allure.feature('流量监测')
@allure.story('获取跨线实时分组状态')
def test_6103_real_status_groups_cross(status_api):
    try:
        my_status = status_api('cross_channel_1')
        res = my_status.status_group_cross()
        assert res.get('rows')
    except Exception as e:
        raise e


@allure.severity('critical')
@allure.feature('流量监测')
@allure.story('获取跨线实时任务状态')
def test_6104_real_status_tasks_cross(status_api):
    try:
        my_status = status_api('cross_channel_1', 'cross_channel_2')
        res = my_status.status_channel_cross()
        assert res.get('additional').get('allUpPeopleCount')
    except Exception as e:
        raise e

