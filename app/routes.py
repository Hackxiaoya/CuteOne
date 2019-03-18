# -*- coding:utf-8 -*-
#从app模块中即从__init__.py中导入创建的app应用
import app
from app.admin import admin as admin_blueprint
from app.main.index import index




"""
    后台
"""
app.app.register_blueprint(admin_blueprint, url_prefix='/admin')


"""
    前台
"""
app.app.register_blueprint(index, url_prefix='/')  # 注册蓝图 - 首页