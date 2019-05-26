# -*- coding:utf-8 -*-
#从app模块中即从__init__.py中导入创建的app应用
import app
from config import TEMPLATES_DIR, STATICFILES_DIR
from flask import render_template
from .main.install import index as install
from .admin import admin as admin_blueprint
from .main import index as index_blueprint


@app.app.errorhandler(404)
def miss(e):
    return render_template('error/404.html'), 404


@app.app.errorhandler(500)
def error(e):
    return render_template('error/404.html'), 500



"""
    安装程序
"""
app.app.register_blueprint(install, url_prefix='/install', template_folder=TEMPLATES_DIR, static_folder=STATICFILES_DIR)


"""
    后台
"""
app.app.register_blueprint(admin_blueprint, url_prefix='/admin', template_folder=TEMPLATES_DIR, static_folder=STATICFILES_DIR)


"""
    前台
"""
app.app.register_blueprint(index_blueprint, url_prefix='/', template_folder=TEMPLATES_DIR, static_folder=STATICFILES_DIR)
