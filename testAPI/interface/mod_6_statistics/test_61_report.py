# coding = utf-8
import pytest
import allure
from datetime import datetime, timedelta
from testAPI.interface.conftest import auth_login, auth_logout


@allure.severity('critical')
@allure.feature('诊断报告')
@allure.story('人群获取实时诊断报告')
def test_6101_get_real_report(stat_api):
    try:
        my_stat = stat_api('crowd_channel_6')
        end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start = (datetime.now() - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
        rep = my_stat.get_real_report(start, end, 'real')
        assert rep.get('checkTime') == '1分钟0秒'
    except Exception as e:
        raise e


@allure.severity('critical')
@allure.feature('诊断报告')
@allure.story('人群获取深度诊断报告')
def test_6102_get_deep_report(stat_api):
    try:
        my_stat = stat_api('crowd_channel_6')
        end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        rep = my_stat.get_real_report(start, end, 'deep')
        # assert rep.get('checkTime') == '1天'
    except Exception as e:
        raise e


@allure.severity('critical')
@allure.feature('诊断报告')
@allure.story('跨线获取实时诊断报告')
def test_6103_get_real_report_cross(stat_api):
    try:
        my_stat = stat_api('cross_channel_1')
        end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start = (datetime.now() - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
        rep = my_stat.getCrossLineReportResult(start, end, 'real')
        assert rep.get('channelId') == my_stat.channel_ids[0]
    except Exception as e:
        raise e


@allure.severity('critical')
@allure.feature('诊断报告')
@allure.story('跨线获取深度诊断报告')
def test_6104_get_deep_report_cross(stat_api):
    try:
        my_stat = stat_api('cross_channel_1')
        end = datetime.now().strftime("%Y-%m-%d %H:%M")
        start = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        rep = my_stat.getCrossLineReportResult(start, end, 'deep')
        assert rep.get('channelId') == my_stat.channel_ids[0]
    except Exception as e:
        raise e