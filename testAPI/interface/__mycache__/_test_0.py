# coding = utf-8
import pytest
# class FooParent(object):
#     def __init__(self, login):
#         self.parent = 'I\'m the parent.'
#         self.login = login
#         print('Parent')
#
#     def xo(self):
#         print(self.login)
#
#
# class FooChild(FooParent):
#     def __init__(self, login):
#         super(FooChild, self).__init__(login)  # 使用super函数
#         print('Child')
#
#     @classmethod
#     def xx(cls, x):
#         cls.x = x
#
#     def oo(self):
#         self.xx(12)
#
#     @classmethod
#     def save_video(cls, video_server):
#         cls.save_rtsp(cls(), 4)
#
#     def save_rtsp(self, json):
#         self.xo()
#         print(json)
#
#
#
#
#
# @pytest.fixture()
# def clear(xx):
#     yield
#     print(xx)
#
#
# def test_clear(clear):
#     xx = 'dsdssd'


# @pytest.fixture
# def make_customer_record():
#
#     created_records = []
#
#     def _make_customer_record(name):
#         record = {
#             "name": name,
#             "orders": []
#         }
#         created_records.append(record)
#         return created_records
#
#     yield _make_customer_record
#
#     for record in created_records:
#         print(record)
#
#
# def test_customer_records(make_customer_record):
#     customer_1 = make_customer_record("Lisa")
#     customer_2 = make_customer_record("Mike")
#     customer_3 = make_customer_record("Meredith")
#     print(customer_3)


#=================================================================================
# # coding = utf-8
# # content of conftest.py
# import pytest
# import smtplib
#
#
# @pytest.fixture(scope="module")
# def smtp_connection(request):
#     server = getattr(request.module, "smtpserver", "smtp.gmail.com")
#     smtp_connection = smtplib.SMTP(server, 587, timeout=5)
#     yield smtp_connection
#     print("finalizing %s (%s)" % (smtp_connection, server))
#     smtp_connection.close()
#
# # content of test_anothersmtp.py
#
# smtpserver = "mail.python.org"  # will be read by smtp fixture
#
# def test_showhelo(smtp_connection):
#     assert 0, smtp_connection.helo()
#
#=================================================================================

# # @file: data.py
# import random
# from collections import namedtuple
#
# Student = namedtuple('Student', ['id', 'ans'])
#
# N_Questions = 25
# N_Students = 20
#
# def gen_random_list(opts, n):
#     return [random.choice(opts) for i in range(n)]
#
# # 问题答案 'ABCD' 随机
# ANS   = gen_random_list('ABCD', N_Questions)
# # 题目分值 1~5 分
# SCORE = gen_random_list(range(1,6), N_Questions)
#
# QUIZE = zip(ANS, SCORE)
# students = [
#     # 学生答案为 'ABCD*' 随机，'*' 代表未作答
#     Student(_id, gen_random_list('ABCD*', N_Questions))
#     for _id in range(1, N_Students+1)
# ]
#
# print(QUIZE)
# # [('A', 3), ('B', 1), ('D', 1), ...
# print(students)
# # [Student(id=1, ans=['C', 'B', 'A', ...


#################################################################################


# from utils.client import HTTPClient
# from utils.config import Config
# from utils.support import encrypt
# from utils.extractor import JMESPathExtractor
#
# base_url = Config().get('BASE_URL', index=0)
#
#
# @pytest.fixture(scope='session')
# def login_admin():
#     """初始化管理员，获取token"""
#
#     api_url = "/api/auth"
#     method = 'POST'
#     JSON = {"username": 'admin', "password": encrypt('Crowd@ad123')}
#     httpcode = [200]
#     extractor = 'token'
#
#     client = HTTPClient(url=(base_url+api_url), method=method)
#     res = client.send(json=JSON)
#
#     assert res.status_code in httpcode
#
#     res = JMESPathExtractor().extract(extractor, res.text) if extractor else res
#     yield res
#
#     client.close()
#
#
# print(login_admin())

#################################################################################