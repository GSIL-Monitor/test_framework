# coding = utf-8
# api-接口请求， ext-结果提取处理， ast-自定义断言
import os
import json
import time
import pytest
import allure
from utils.config import Config
from utils.log import logger
from utils.sql import Sql
from utils.support import encrypt
from testAPI.common.pre_request import PRequest
from testAPI.common.pre_sql_data import *
from testAPI.interface import conftest


__all__ = (
    'APIStat'
)


@pytest.fixture(scope='session')
def stat_api(login_admin, task_env):
    my_stat = APIStat(login_admin)

    def parse_api_stat(*channel):
        my_stat.channel_ids = [task_env(ch).channelId for ch in channel]
        return my_stat
    return parse_api_stat


class APIStat(PRequest):
    """
    用户接口类
    """

    def __init__(self, login=None):
        # 初始化入参
        super(APIStat, self).__init__(login)
        # 初始化类属性
        self.channel_ids = None

    @allure.step('api - 1. 获取人群实时诊断报告')
    def get_real_report(self, start, end, type, status='PASS'):
        """
        :param type: real, deep (时间精确到秒）
        """
        api_url = "/api/realreport/getReport"
        method = 'POST'
        data = {'channelId': self.channel_ids[0], 'startDate': start, 'endDate': end, 'checkType': type}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 2. 人群统计图')
    def stat_status_by_minute(self, start, end, stat_type, time_type, status='PASS'):
        """
        statType: 'population'(人员数量), 'density'(密度), 'safety'(安全指数)
        time_type: 10, 30, 60
        """
        api_url = "/api/statistic/stat-status-by-minute"
        method = 'POST'
        data = {'channelIds': self.channel_ids, 'startDate': start, 'endDate': end, 'statType': stat_type, 'timeType': time_type}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 3. 人群统计表')
    def list_status_by_minute(self, start, end, stat_type, time_type, status='PASS'):
        """
        statType: 'population'(人员数量), 'density'(密度), 'safety'(安全指数)
        time_type: 10, 30, 60
        """
        api_url = "/api/statistic/list-status-by-minute"
        method = 'POST'
        data = {
            'channelIds': self.channel_ids, 'startDate': start, 'endDate': end, "nd": int(time.time()*1000),
            'statType': stat_type, 'timeType': time_type, "_search": "false", "rows": 10, "page": 1, "sidx": None,
            'sord': 'asc'
        }
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 4. 事件类型统计')
    def stat_event_type(self, task_type, query_type, num=0, status='PASS'):
        """
        :param task_type: "Crowd", 'CrossLine'
        :param query_type: oneDay, oneWeek, oneMonth
        :param num: 默认为0，代表当天/当周/当月，为1则代表昨天/上周/上月，以此类推
        """
        api_url = "/api/statistic/stat-event-type"
        method = 'POST'
        data = {'channelId': ','.join(self.channel_ids), 'taskType': task_type, 'queryType': query_type, "lang": 'zh-cn', 'pagenum': num}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 5. 事件查询初始化？')
    def list_event_init(self, start, end, status='PASS'):
        api_url = "/api/event/list-event-init"
        method = 'POST'
        data = {'channelId': self.channel_ids[0], 'startDate': start, 'endDate': end, "eventType": None}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 6. 事件查询')
    def list_event(self, start, end, event_type, task_type, status='PASS'):
        """
        :param task_type: "Crowd", "CrossLine"
        :param event_type: Crowded, Gather, Retention, Chaos, Retrograde, TRAFFIC_EVENT 字符串形式逗号隔开
        """
        api_url = "/api/event/list-event"
        method = 'POST'
        search = {
            "taskType": task_type,
            "eventTypes": event_type,
            "startDate": start,
            "endDate": end,
            "channelIds": ','.join(self.channel_ids)
        }
        data = {'searchString': json.dumps(search),  "nd": int(time.time()*1000),
                "_search": "false", "rows": 4, "page": 1, "sidx": 'dateTime', "sord": "desc"}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 7. 导出统计报表1')
    def export_status_by_minute(self, start, end, stat_type, time_type, status='PASS'):
        """
        statType: 'population'(人员数量), 'density'(密度), 'safety'(安全指数)
        time_type: 10, 30, 60
        """
        api_url = "/api/statistic/export-status-by-minute"
        method = 'POST'
        data = {'channelIds': self.channel_ids, 'startDate': start, 'endDate': end, 'statType': stat_type, 'timeType': time_type}
        res = self.send_request(api_url, method, status, data=data, extractor='ext')
        return res

    @allure.step('api - 7. 导出统计报表2')
    def export_file_stat(self, req_name, file_path, status='PASS'):
        """
        statType: 'population'(人员数量), 'density'(密度), 'safety'(安全指数)
        time_type: 10, 30, 60
        """
        api_url = "/export/{}".format(req_name)
        method = 'GET'
        res = self.send_request(api_url, method, status)

        abs_exp_file = Config(file_path).file
        with open(abs_exp_file, 'wb') as exp:
            exp.write(res.content)
        assert os.path.getsize(abs_exp_file)
        return abs_exp_file

    @allure.step('api - 8. 跨线统计图-进出流量')
    def stat_people_flow_rate(self, start, end, stat_type, time_type, status='PASS'):
        """
        statType: 'PeopleFlowRate'(进出流量统计)
        time_type: 10, 30, 60
        """
        api_url = "/api/statistic/stat-people-flow-rate"
        method = 'POST'
        data = {'channelIds': self.channel_ids, 'startDate': start, 'endDate': end, 'statType': stat_type, 'timeType': time_type}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 9. 跨线统计表-进出流量')
    def people_flow_rate_list(self, start, end, stat_type, time_type, status='PASS'):
        """
        statType: 'PeopleFlowRate'(进出流量统计)
        time_type: 10, 30, 60
        """
        api_url = "/api/statistic/people-flow-rate-list"
        method = 'POST'
        data = {
            'channelIds': self.channel_ids, 'startDate': start, 'endDate': end, "nd": int(time.time()*1000),
            'statType': stat_type, 'timeType': time_type, "_search": "false", "rows": 10, "page": 1, "sidx": None,
            'sord': 'asc'
        }
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 10. 跨线统计图-进出人次')
    def statInOrOutCount(self, start, end, stat_type, time_type, status='PASS'):
        """
        statType: 'InAndOutStatistics'(进出人次统计)
        time_type: 10, 30, 60
        """
        api_url = "/api/statistic/statInOrOutCount"
        method = 'POST'
        data = {'channelIds': self.channel_ids, 'startDate': start, 'endDate': end, 'statType': stat_type, 'timeType': time_type}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 11. 跨线统计表-进出人次')
    def getInOrOutCount(self, start, end, stat_type, time_type, status='PASS'):
        """
        statType: 'InAndOutStatistics'(进出人次统计)
        time_type: 10, 30, 60
        """
        api_url = "/api/statistic/getInOrOutCount"
        method = 'POST'
        data = {
            'channelIds': self.channel_ids, 'startDate': start, 'endDate': end, "nd": int(time.time()*1000),
            'statType': stat_type, 'timeType': time_type, "_search": "false", "rows": 10, "page": 1, "sidx": None,
            'sord': 'asc'
        }
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 12. 进出对比图：人次-流量')
    def getComparisonResult(self, start, end, stat_type, time_type, status='PASS'):
        """
        statType: 'MultipleCamerasComparison'(进出人次对比), 'MultipleCamerasUpFlowRate'(进出流量对比)
        time_type: 10, 30, 60
        """
        api_url = "/api/statistic/getComparisonResult"
        method = 'POST'
        data = {'channelIds': self.channel_ids, 'startDate': start, 'endDate': end, 'statType': stat_type, 'timeType': time_type}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 13. 进出对比表：人次-流量')
    def getComparisonList(self, start, end, stat_type, time_type, status='PASS'):
        """
        statType: 'MultipleCamerasComparison'(进出人次对比), 'MultipleCamerasUpFlowRate'(进出流量对比)
        time_type: 10, 30, 60
        """
        api_url = "/api/statistic/getComparisonList"
        method = 'POST'
        data = {
            'channelIds': self.channel_ids, 'startDate': start, 'endDate': end, "nd": int(time.time()*1000),
            'statType': stat_type, 'timeType': time_type, "_search": "false", "rows": 10, "page": 1, "sidx": None,
            'sord': 'asc'
        }
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 14. 获取跨线实时诊断报告')
    def getCrossLineReportResult(self, start, end, type, status='PASS'):
        """
        :param type: real, deep (时间精确到秒）
        """
        api_url = "/api/realreport/getCrossLineReportResult"
        method = 'POST'
        data = {'channelId': self.channel_ids[0], 'startTime': start, 'endTime': end, 'reportType': type}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

    @allure.step('api - 15. 获取跨线深度诊断报告')
    def getCrossLineReportResult(self, start, end, type, status='PASS'):
        """
        :param type: real, deep (时间精确到秒）
        """
        api_url = "/api/realreport/getCrossLineReportResult"
        method = 'POST'
        data = {'channelId': self.channel_ids[0], 'startTime': start, 'endTime': end, 'reportType': type}
        res = self.send_request(api_url, method, status, data=data)
        logger.debug(res.json())
        return res.json()

