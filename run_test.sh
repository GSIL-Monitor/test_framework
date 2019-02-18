#!/bin/bash
set -x

ROOTPATH=$(cd `dirname $0`; pwd)

echo "安装python3"
yum install -y python3 || apt install -y python3

echo "安装pip3"
pip3 -V || { 
    wget https://bootstrap.pypa.io/3.2/get-pip.py;
    python3 get-pip.py
    }

echo "安装pipenv"
pipenv --version || pip3 install  -U pipenv

echo "切换路径"
cd $ROOTPATH && pwd && ls

echo "安装虚拟环境+依赖模块"
pipenv run pip install pip==18.0
pipenv install --skip-lock

echo "执行pytest"
pipenv run pytest  testAPI/interface/video/ --alluredir allure-results
