#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from ftplib import FTP

args = len(sys.argv)
if args >= 2:
    download_path = sys.argv[1]


class MyFTP(FTP):
    def __init__(self):
        self.ftp = FTP().__init__()
        self.release_dir = ''  # 远程服务器版本包所在父目录
        self.latest_path = ''  # 远程服务器最新版本包，绝对路径
        self.latest_file = ''  # 远程服务器最新版本包，名称
        self.local_file = ''   # 本地下载版本包，绝对路径

    def login(self, server, user, passwd):
        """登录ftp服务器"""
        self.ftp = FTP(server)
        self.ftp.login(user, passwd)
        print("Logon success---------->")

    def get_latest(self, release_dir):
        """
        获取最新文件名称
        ftp.nlst(dir) 获取dir目录下所有文件的绝对路径列表
        """
        self.latest_path = self.ftp.nlst(release_dir)[len(self.ftp.nlst(release_dir)) - 1]
        self.latest_file = self.latest_path.split('/')[-1]

    def check(self, local_path):
        """检测本地是否存在文件，已存在则不再下载"""
        self.local_file = os.path.join(local_path, self.latest_file)
        if os.path.isfile(self.local_file):
            return True
        else:
            return False

    def down_latest(self):
        """下载最新文件：
        执行get_latest(远程指定目录下），获取最新文件
        执行check（本地目录，最新文件），获取下载文件绝对路径，并检查存在与否
        执行down_latest,自动下载远程目录下最新文件，到本地目录下的绝对文件路径
        retrbinary（远程文件相对路径，本地文件绝对路径）
        """
        print("Download %s from %s to %s" % (self.latest_file, self.latest_path, self.local_file))
        self.ftp.retrbinary('RETR %s' % self.latest_path, open(self.local_file, 'wb').write)

    def quit(self):
        print("End connect------------>")
        self.ftp.quit()


if __name__ == '__main__':
    release_dir = '/binnary'  # ftp服务器下载目录
    local_path = '/home/FdsInstall'  # 本地保存目录

    ftp = MyFTP()
    ftp.login('10.100.2.16', 'ftp', '123456')
    ftp.get_latest(release_dir)

    if not ftp.check(local_path):
        os.system('rm -rf {0};mkdir -p {0}'.format(local_path))
        ftp.down_latest()
        os.system('unzip {0} -d {1}'.format(ftp.local_file, local_path))
        ftp.quit()
    else:
        ftp.quit()
        raise IOError("You have got the latest version!")







