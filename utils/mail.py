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
from utils.log import logger
from utils.config import Config, REPORT_PATH


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
        logger.info('attach file {}'.format(att_file))

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
            logger.error('发送邮件失败，无法链接smtp服务器，检查网络或服务器. %s' % e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                logger.error('用户名密码验证失败！%s' % e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送
                logger.info('发送邮件"{title}"成功! 收件人：{receiver}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(title=self.title, receiver=self.receiver))
            finally:
                smtp_server.quit()  # 断开


def send_report():
    _email = Config().get('email', index=1)
    title = _email.get('title')
    receiver = _email.get('receiver')
    server = _email.get('server')
    port = _email.get('port')
    sender = _email.get('sender')
    password = _email.get('password')
    ssl = _email.get('ssl')

    # REPORT_NAME = '{}-report.html'.format(time.strftime('%Y-%m-%d-%H-%M-%S'))
    REPORT_NAME = 'report.html'
    report = os.path.join(REPORT_PATH, REPORT_NAME)

    message1 = '这是今天的测试报告'
    message2 = open(report, 'r', encoding='utf-8').read()

    e = Email(title=title, receiver=receiver, server=server,
              sender=sender, port=port, password=password, ssl=ssl,
              path=report,
              message='{0}\n{1}'.format(message1, message2)
              )
    e.send()


if __name__ == '__main__':
    send_report()


