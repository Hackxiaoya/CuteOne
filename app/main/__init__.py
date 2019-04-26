# -*- coding:utf-8 -*-
from flask import Blueprint, session
from app.admin.system import models as systemModels

index = Blueprint('/', __name__)  # 创建一个蓝图对象，设置别名


# 基本配置
@index.context_processor
def webconfig():
    webconfig = systemModels.config.all()
    webconfig.pop('username')
    webconfig.pop('password')
    return dict(webconfig=webconfig)



from .indexs import views
from .users import views


