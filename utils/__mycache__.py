# !/usr/bin/python
# -*- coding: UTF-8 -*-

"""
邮件类。给指定用户发邮件。多个发件人和附件
"""
import os
import re
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
from sys import argv

# store_IP = argv[1]
# store_Path = argv[2]
# version = argv[3]
# pack_Dir = argv[4]
# release_Note = argv[5]
# Project_Name = argv[6]
# branchVer = open("% s/version.txt" % pack_Dir, 'r').read()
store_IP = '172.17.3.126'
store_Path = 'CrowdProduct_Store\\CrowdPackage\\v4.2.0\\20190109104411'
version = 'v4.2.0'
release_Note = 'TEST RELEASE'
Project_Name = 'CrowdProduct'
branchVer = 'v4.2.0.1023'

server = 'mail.sensenets.cn'
port = 25
ssl = False

sender = 'zhangjiukun@sensenets.cn'
password = 'sensenets'

title = "【%s】【%s】Product build success, please test." % (Project_Name, version)

message = '<br>【Package Path】</br><br>\\\\{}{}</br>【Version Info】<br><pre>{}</pre></br>【Release Notes】<br><pre>{}</pre></br>'. \
    format(store_IP, store_Path, branchVer, release_Note)

# receiver = "tanghao@sensenets.com;yangpengyan@sensenets.com;" \
#            "hupanbpan@sensenets.com;zhangjiukun@sensenets.com;" \
#            "lixiaohui@sensenets.com;shenshuyu@sensenets.com"
receiver = 'zhangjiukun@sensenets.com;850871592@qq.com;zhangjiukun@sensenets.cn'


class Email:
    def __init__(self, server, port, sender, password, receiver, title, message=None, path=None, ssl=True):
        """初始化Email
        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径（list or str），非必填。
        :param server: smtp服务器，必填。
        :param port: smtp端口，必填（ssl默认465，非ssl默认25）。
        :param ssl: True or False，默认True。
        :param sender: 发件人，必填。
        :param password: 密码，必填
        :param receiver: 收件人，多个收件人“ ；”隔开，必填
        """
        self.title = title
        self.message = message
        self.files = path

        self.msg = MIMEMultipart('related')

        self.server = server
        self.port = port
        self.sender = sender
        self.receiver = receiver
        self.password = password
        self.ssl = ssl

    def _attach_file(self, att_file):
        """添加单个文件到附件列表"""
        file_name = re.split(r'[\\|/]', att_file)
        att = MIMEText(open(att_file, 'rb').read(), 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["content-Disposition"] = 'attachment;filename="%s"' % file_name[-1]
        self.msg.attach(att)
        print('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 正文
        if self.message:
            self.msg.attach(MIMEText(self.message, 'html', 'utf-8'))

        # 附件
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        # 发送
        try:
            if self.ssl:
                smtp_server = smtplib.SMTP_SSL(self.server, self.port)
            else:
                smtp_server = smtplib.SMTP(self.server, self.port)
                smtp_server.ehlo()
                smtp_server.starttls()
        except (gaierror or error) as e:
            print('发送邮件失败，无法链接smtp服务器，检查网络或服务器. %s' % e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                print('用户名密码验证失败！%s' % e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送
                print('发送邮件"{title}"成功! 收件人：{receiver}。如果没有收到邮件，请检查垃圾箱，'
                      '同时检查收件人地址是否正确'.format(title=self.title, receiver=self.receiver))
            finally:
                smtp_server.quit()  # 断开


def send_report():
    e = Email(title=title, receiver=receiver, server=server,
              sender=sender, port=port, password=password, ssl=False,
              path=None,
              message=message
              )
    e.send()


if __name__ == '__main__':
    send_report()


#
# # !/usr/bin/python
# # -*- coding: UTF-8 -*-
#
# """
# 邮件类。给指定用户发邮件。多个发件人和附件
# """
# import os
# import re
# import time
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from socket import gaierror, error
# from sys import argv
#
# # store_IP = argv[1]
# # store_Path = argv[2]
# # version = argv[3]
# # pack_Dir = argv[4]
# # release_Note = argv[5]
# # Project_Name = argv[6]
# # branchVer = open("% s/version.txt" % pack_Dir, 'r').read()
# # strTo = ['tanghao@sensenets.com', 'yangpengyan@sensenets.com',
# #          'zhangjiukun@sensenets.com', 'hupanbpan@sensenets.com',
# #          'lixiaohui@sensenets.com', 'shenshuyu@sensenets.com'
# #         ]  # --收件人列表
#
#
# store_IP = '172.17.3.126'
# store_Path = 'CrowdProduct_Store\\CrowdPackage\\v4.2.0\\20190109104411'
# version = 'v4.2.0'
# release_Note = 'TEST RELEASE'
# Project_Name = 'CrowdProduct'
# branchVer = 'v4.2.0.1023'
#
#
# class Email:
#     def __init__(self, server, port, sender, password, receiver, title, message=None, path=None, ssl=True):
#         """初始化Email
#
#         :param title: 邮件标题，必填。
#         :param message: 邮件正文，非必填。
#         :param path: 附件路径（list or str），非必填。
#         :param server: smtp服务器，必填。
#         :param sender: 发件人，必填。
#         :param password: 密码，必填
#         :param receiver: 收件人，多个收件人“ ；”隔开，必填
#         """
#         self.title = title
#         self.message = message
#         self.files = path
#
#         self.msg = MIMEMultipart('related')
#
#         self.server = server
#         self.port = port
#         self.sender = sender
#         self.receiver = receiver
#         self.password = password
#         self.ssl = ssl
#
#     def _attach_file(self, att_file):
#         """添加单个文件到附件列表"""
#         file_name = re.split(r'[\\|/]', att_file)
#         att = MIMEText(open(att_file, 'rb').read(), 'plain', 'utf-8')
#         att["Content-Type"] = 'application/octet-stream'
#         att["content-Disposition"] = 'attachment;filename="%s"' % file_name[-1]
#         self.msg.attach(att)
#         print('attach file {}'.format(att_file))
#
#     def send(self):
#         self.msg['Subject'] = self.title
#         self.msg['From'] = self.sender
#         self.msg['To'] = self.receiver
#
#         # 正文
#         if self.message:
#             self.msg.attach(MIMEText(self.message, 'html', 'utf-8'))
#
#         # 附件
#         if self.files:
#             if isinstance(self.files, list):
#                 for f in self.files:
#                     self._attach_file(f)
#             elif isinstance(self.files, str):
#                 self._attach_file(self.files)
#
#         # 发送
#         try:
#             if self.ssl:
#                 smtp_server = smtplib.SMTP_SSL(self.server, self.port)
#             else:
#                 smtp_server = smtplib.SMTP(self.server, self.port)
#                 smtp_server.ehlo()
#                 smtp_server.starttls()
#         except (gaierror or error) as e:
#             print('发送邮件失败，无法链接smtp服务器，检查网络或服务器. %s' % e)
#         else:
#             try:
#                 smtp_server.login(self.sender, self.password)  # 登录
#             except smtplib.SMTPAuthenticationError as e:
#                 print('用户名密码验证失败！%s' % e)
#             else:
#                 smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送
#                 print('发送邮件"{title}"成功! 收件人：{receiver}。如果没有收到邮件，请检查垃圾箱，'
#                       '同时检查收件人地址是否正确'.format(title=self.title, receiver=self.receiver))
#             finally:
#                 smtp_server.quit()  # 断开
#
#
# def send_report():
#
#     title = "【%s】【%s】Product build success, please test." % (Project_Name, version)
#     receiver = 'zhangjiukun@sensenets.com;850871592@qq.com'
#     server = 'mail.sensenets.cn'
#     sender = 'zhangjiukun@sensenets.cn'
#     password = 'sensenets'
#     port = 25
#
#     message1 = '【Package Path】<br>\\\\{}{}</br>【Version Info】<br>{}</br>【Release Notes】<br>{}</br>'.\
#         format(store_IP, store_Path, branchVer, release_Note)
#
#     e = Email(title=title, receiver=receiver, server=server,
#               sender=sender, port=port, password=password, ssl=False,
#               path=None,
#               message=message1
#               )
#     e.send()
#
#
# if __name__ == '__main__':
#     send_report()
#
#
