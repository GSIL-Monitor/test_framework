#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from utils.log import logger
from utils.config import Config

class Sql(object):
    def __init__(self):
        _config = Config().get('sql')
        self.sql_server = _config.get('sql_server')
        self.sql_port = _config.get('sql_port')
        self.sql_name = _config.get('sql_name')
        self.sql_user = _config.get('sql_user')
        self.sql_password = _config.get('sql_password')
        self.connect()
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    def connect(self):
        logger.info('连接到mysql服务器{}'.format(self.sql_server))
        self.db = mysql.connector.connect(host=self.sql_server, port=self.sql_port,
                                          user=self.sql_user, passwd=self.sql_password,
                                          database=self.sql_name, use_unicode=True)
        return self.db

    def exec(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logger.info('执行成功')
        except:
            logger.error('执行失败，回滚数据库')
            self.db.rollback()

    def query(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            logger.info('查询结果为：{}'.format(results))
            return results
        except:
            logger.error("Error: unable to fecth data")

    def close(self):
        self.db.close()


if __name__ == '__main__':
    query_camera_count = "SELECT COUNT(*) FROM t_video_channel " \
                         "WHERE F_Video_Server_ID = '2C1DCDF3E6B44B4F9A42568041B27594' " \
                         "AND F_Enabled = 1;"
    mysql = Sql()
    count = mysql.query(query_camera_count)[0][0]
    logger.info(count)
