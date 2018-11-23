"""
邮件类。给指定用户发邮件。多个发件人和附件
"""
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
from utils.log import logger


class Email:
    def __init__(self, server, sender, password, receiver, title, message=None, path=None):
        """初始化Email

        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径（list or str），非必填。
        :param server: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 密码，必填
        :param receiver: 收件人，多个收件人“ ；”隔开，必填
        """
        self.title = title
        self.message = message
        self.files = path

        self.msg = MIMEMultipart('related')

        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.password = password

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
            smtp_server = smtplib.SMTP_SSL(self.server)
        except (gaierror or error) as e:
            logger.exception('发送邮件失败，无法链接smtp服务器，检查网络或服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送
            finally:
                smtp_server.quit()  # 断开
                logger.info('发送邮件"{title}"成功! 收件人：{receiver}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(title=self.title, receiver=self.receiver))


if __name__ == '__main__':
    message1 = '这是今天的测试报告'
    message2 = open('../report/report.html', 'r', encoding='utf-8').read()
    e = Email(title='搜索功能测试报告',
              message='{0}\n{1}'.format(message1, message2),
              receiver='zhangjiukun@sensenets.com',
              server='smtp.exmail.qq.com:465',
              sender='zhangjiukun@sensenets.com',
              password='Sensenets1992',
              path='../report/report.html'
              )
    e.send()




