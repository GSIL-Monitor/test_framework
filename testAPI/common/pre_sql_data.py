# coding = utf-8

from utils.sql import Sql
from utils.config import Config
from utils.log import logger

__all__ = (
    'load_video_data',
    'load_task_data',
    'load_group_data',
    'load_user_data',
    'clear_all'
)

abs_sql_video_server = Config('data/sql/t_video_server.sql').file
abs_sql_video_group = Config('data/sql/t_video_group.sql').file
abs_sql_video_channel = Config('data/sql/t_video_channel.sql').file

abs_sql_task = Config('data/sql/t_task.sql').file

abs_sql_custom_group = Config('data/sql/t_custom_group.sql').file
abs_sql_custom_cameras_group = Config('data/sql/t_custom_cameras_group.sql').file

abs_sql_role_model = Config('data/sql/t_role_model.sql').file
abs_sql_user = Config('data/sql/t_user.sql').file

abs_sql_init_all = Config('data/sql/init.sql').file


def load_video_data():
    sql = Sql()
    logger.info("载入SQL数据中……")
    sql.load_sql(abs_sql_video_server)
    sql.load_sql(abs_sql_video_group)
    sql.load_sql(abs_sql_video_channel)
    logger.info("载入完成")
    sql.close()


# def query_video_id(video_name):
#     sql = Sql()
#     sql_video_id = "SELECT F_ID FROM t_video_server " \
#                    "WHERE F_NAME = '{}' " \
#                    "AND F_Enabled = 1;".format(video_name)
#
#     server_id = sql.query(sql_video_id)[0][0] if sql.query(sql_video_id)[0] else None
#     sql.close()
#     return server_id


def load_task_data():
    sql = Sql()
    logger.info("载入SQL数据中……")
    sql.load_sql(abs_sql_task)  # 人群任务的前后端同步机制，造成这里导入数据之后，任务的默认状态只能是fail，需要间隔一会儿自动变成run
    logger.info("载入完成")
    sql.close()


def load_group_data():
    sql = Sql()
    logger.info("载入SQL数据中……")
    sql.load_sql(abs_sql_custom_group)
    sql.load_sql(abs_sql_custom_cameras_group)
    logger.info("载入完成")
    sql.close()


def load_user_data():
    sql = Sql()
    logger.info("载入SQL数据中……")
    sql.load_sql(abs_sql_role_model)
    sql.load_sql(abs_sql_user)
    logger.info("载入完成")
    sql.close()


def clear_all():
    sql = Sql()
    sql.load_sql(abs_sql_init_all)
    sql.close()

