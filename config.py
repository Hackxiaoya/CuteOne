# -*- coding:utf-8 -*-
import os

BASE_DIR = os.getcwd()  # 项目的绝对路径
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')  # 模板文件的路径
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')  # 静态文件的路径

SECRET_KEY =  os.urandom(24) # 随机产生24位的字符串作为SECRET_KEY,web重启就会变化

"""
    版本信息
"""
SystemInfo = {
    "name": "CuteOne",
    "versionType": "Free",
    "versions": "1.0.0",
    "server": ""
}




"""
    Mysql 数据库连接信息
"""
SQLALCHEMY_DATABASE_URI = ""
SQLALCHEMY_POOL_SIZE = 100
# SQLALCHEMY_POOL_TIMEOUT = 1
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True
SQLALCHEMY_ECHO = False  # 打印SQL语句 True or False


"""
    MongoDB 数据库链接信息
"""
MONGO_URI = ""



"""
    OneDrive API设置
"""
BaseAuthUrl = "https://login.microsoftonline.com"
app_url = "https://graph.microsoft.com/"