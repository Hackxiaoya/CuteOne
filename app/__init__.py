# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo


#创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
app.config.from_object('config')
MysqlDB = SQLAlchemy(app)
MongoDB = PyMongo(app)



# 蓝图注册路由文件
from app import routes