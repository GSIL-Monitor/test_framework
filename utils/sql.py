#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from utils.log import logger
from utils.config import Config
import datetime
import time
import os
from utils.error import Sqlerror


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
            logger.info('sql执行成功')
        except:
            err = 'sql执行失败，回滚数据库'
            logger.error(err)
            self.db.rollback()
            raise Sqlerror(err)

    def query(self, sql):
        try:
            self.cursor.execute(sql)

            results = []
            row = self.cursor.fetchone()
            while row is not None:
                # logger.debug(row)
                results.append(row)
                row = self.cursor.fetchone()

            # results = self.cursor.fetchall()
            # logger.debug('查询结果为：{}'.format(results))
            return results
        except:
            err = "Error: unable to fecth data"
            logger.error(err)
            raise Sqlerror(err)

    def load_sql(self, abs_sql_file):
        """
        Load sql file to mysql server.
        Sql file must only contains sql cmd (not support comment), every cmd should end with ';' and a line break.
        注意：这里埋了一个坑，sql文件如果结尾处没有空行，执行不成功且不会报错
        """
        logger.debug("load {} ".format(abs_sql_file))
        with open(abs_sql_file, 'r', encoding='utf-8') as file_sql:
            file_sql_video = file_sql.read().split(';\n')[:-1]
            # logger.debug(sql_video)
            sql_list = [x.replace('\n', '') if '\n' in x else x for x in file_sql_video]
            # logger.debug(sql_list)

        for sql_item in sql_list:
            self.exec(sql_item)

    # def assert_query(self, sql, exp):
    #
    #     logger.info(sql)
    #
    #     # 循环检查并断言camera数量
    #     init = -1
    #     start = datetime.datetime.now()
    #     while True:
    #         try:
    #             query_res = self.query(sql)[0][0]
    #             now = datetime.datetime.now()
    #             interval = (now - start).seconds
    #             if query_res == exp or query_res is exp:
    #                 logger.info('查询完毕，结果匹配')
    #                 res = 'SUCCESS'
    #                 break
    #             elif query_res == init and interval > 30:
    #                 logger.error('查询完毕，结果不匹配')
    #                 res = 'FAIL'
    #                 break
    #             else:
    #                 init = query_res
    #                 logger.info('查询中，已耗时{}，查询结果为{}'.format((now - start), query_res))
    #                 time.sleep(5)
    #         except Exception as e:
    #             logger.error("查询出错：{}".format(e))
    #     end = datetime.datetime.now()
    #     logger.info('总耗时:{}'.format(end - start))
    #     assert res == 'SUCCESS'

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    query_camera_count = "SELECT COUNT(*) FROM t_video_channel " \
                         "WHERE F_Video_Server_ID = '48F992E659E24627BCE3E90BCF3D2A23' " \
                         "AND F_Enabled = 1;"
    mysql = Sql()
    count = mysql.query(query_camera_count)[0][0]
    logger.info(count)
    # mysql.load_sql(Config('data/sql/t_video_channel.sql').file)
    mysql.close()

    # query_camera_count1 = "SELECT F_ID FROM t_video_channel " \
    #                       "WHERE F_Name = '19、上海外滩白天' " \
    #                       "AND F_Video_Server_ID = '08DEF499881748518948557AB48329AC';"
    #
    # count = mysql.query(query_camera_count1)[0][0]
    # logger.info(count)



    #
    # import os
    # from utils.config import Config, BASE_PATH
    # from utils.log import logger
    #
    # CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'apitask.yml')
    # config_video = Config('apitask.yml')
    #
    # task1 = config_video.get("crowd_task_two")
    # camera_name = task1["channelName"]
    # print(camera_name)
    #
    # query_camera_count = "SELECT F_ID FROM t_video_channel " \
    #                      "WHERE F_Name = '{}' " \
    #                      "AND F_Video_Server_ID = '431854A664DD48F3A276F0294BC24601';".format(camera_name)
    #
    # camera_id = mysql.query(query_camera_count)[0][0]
    # print(camera_id)



