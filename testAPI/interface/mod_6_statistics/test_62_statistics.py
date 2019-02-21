# coding = utf-8
import pytest
import allure
from datetime import datetime, timedelta
from testAPI.interface.conftest import auth_login, auth_logout


@allure.severity('normal')
@allure.feature('统计分析')
@allure.story('统计图和统计表：人数-密度-安全指数')
@pytest.mark.parametrize('stat_type', ['population', 'density', 'safety'])
@pytest.mark.parametrize('time_type', [10, 30, 60])
def test_6201_stat_status(stat_api, stat_type, time_type):
    try:
        my_stat = stat_api('crowd_channel_6', 'crowd_channel_1')
        end = datetime.now().strftime("%Y-%m-%d %H:%M")
        start = datetime.now().strftime("%Y-%m-%d 00:00")
        rep = my_stat.stat_status_by_minute(start, end, stat_type, time_type)
        assert rep.get('statResultJson')
        rep2 = my_stat.list_status_by_minute(start, end, stat_type, time_type)
        assert rep2.get('records')
    except Exception as e:
        raise e


@allure.severity('normal')
@allure.feature('统计分析')
@allure.story('统计: 事件类型统计')
@pytest.mark.parametrize('query_type', ['oneDay', 'oneWeek', 'oneMonth'])
@pytest.mark.parametrize('num', [0, 1, 2])
@pytest.mark.parametrize('task, task_type', [('crowd_channel_1', 'Crowd'), ('cross_channel_1', 'CrossLine')])
def test_6203_stat_event_type(stat_api, query_type, num, task, task_type):
    try:
        my_stat = stat_api(task)
        rep = my_stat.stat_event_type(task_type, query_type, num)
        assert rep.get('queryType') == query_type
    except Exception as e:
        raise e


@allure.severity('normal')
@allure.feature('统计分析')
@allure.story('人群事件查询')
@pytest.mark.parametrize('event_type', ['Crowded', 'Gather', 'Retention', 'Chaos', 'Retrograde'])
def test_6204_list_event_crowd(stat_api, event_type):
    try:
        my_stat = stat_api('crowd_channel_6', 'crowd_channel_2')
        end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        rep = my_stat.list_event(start, end, event_type, 'Crowd')
        # assert rep.get('records')
    except Exception as e:
        raise e


@allure.severity('normal')
@allure.feature('统计分析')
@allure.story('跨线事件查询')
@pytest.mark.parametrize('event_type', ['TRAFFIC_EVENT'])
def test_6205_list_event_cross(stat_api, event_type):
    try:
        my_stat = stat_api('crowd_channel_6', 'crowd_channel_2')
        end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        rep = my_stat.list_event(start, end, event_type, 'CrossLine')
        # assert rep.get('records')
    except Exception as e:
        raise e


@allure.severity('normal')
@allure.feature('统计分析')
@allure.story('统计结果导出：人数-密度-安全指数')
@pytest.mark.parametrize('stat_type', ['population', 'density', 'safety'])
@pytest.mark.parametrize('time_type', [10, 30, 60])
def test_6206_export_stat(stat_api, stat_type, time_type):
    try:
        # 获取文件名称
        my_stat = stat_api('crowd_channel_6', 'crowd_channel_1')
        end = datetime.now().strftime("%Y-%m-%d %H:%M")
        start = datetime.now().strftime("%Y-%m-%d 00:00")
        rep = my_stat.export_status_by_minute(start, end, stat_type, time_type)
        assert rep
        file_name = rep.split('/')[1]
        # 导出文件
        my_stat.export_file_stat(rep, 'data/ex_rep/{}'.format(file_name))
    except Exception as e:
        raise e


@allure.severity('normal')
@allure.feature('统计分析')
@allure.story('统计图和统计表：进出流量')
@pytest.mark.parametrize('stat_type', ['PeopleFlowRate'])
@pytest.mark.parametrize('time_type', [10, 30, 60])
def test_6207_stat_people_flow_rate(stat_api, stat_type, time_type):
    try:
        my_stat = stat_api('cross_channel_1', 'cross_channel_2')
        end = datetime.now().strftime("%Y-%m-%d %H:%M")
        start = datetime.now().strftime("%Y-%m-%d 00:00")
        rep = my_stat.stat_people_flow_rate(start, end, stat_type, time_type)
        assert rep.get('statResultJson')
        rep2 = my_stat.people_flow_rate_list(start, end, stat_type, time_type)
        assert rep2.get('records')
    except Exception as e:
        raise e


@allure.severity('normal')
@allure.feature('统计分析')
@allure.story('统计图和统计表：进出人次')
@pytest.mark.parametrize('stat_type', ['InAndOutStatistics'])
@pytest.mark.parametrize('time_type', [10, 30, 60])
def test_6208_statInOrOutCount(stat_api, stat_type, time_type):
    try:
        my_stat = stat_api('cross_channel_1', 'cross_channel_2')
        end = datetime.now().strftime("%Y-%m-%d %H:%M")
        start = datetime.now().strftime("%Y-%m-%d 00:00")
        rep = my_stat.statInOrOutCount(start, end, stat_type, time_type)
        assert rep.get('statResultJson')
        rep2 = my_stat.getInOrOutCount(start, end, stat_type, time_type)
        assert rep2.get('total')
    except Exception as e:
        raise e


@allure.severity('normal')
@allure.feature('统计分析')
@allure.story('统计图和统计表：进出对比')
@pytest.mark.parametrize('stat_type', ['MultipleCamerasComparison', 'MultipleCamerasUpFlowRate'])
@pytest.mark.parametrize('time_type', [10, 30, 60])
def test_6209_getComparisonResult(stat_api, stat_type, time_type):
    try:
        my_stat = stat_api('cross_channel_1', 'cross_channel_2')
        end = datetime.now().strftime("%Y-%m-%d %H:%M")
        start = datetime.now().strftime("%Y-%m-%d 00:00")
        rep = my_stat.getComparisonResult(start, end, stat_type, time_type)
        assert rep[0].get('total')
        rep2 = my_stat.getComparisonList(start, end, stat_type, time_type)
        assert rep2.get('records')
    except Exception as e:
        raise e

