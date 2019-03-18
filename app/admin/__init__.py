# -*- coding:utf-8 -*-
from flask import Blueprint, session
from config import TEMPLATES_DIR, STATICFILES_DIR

admin = Blueprint('admin', __name__, template_folder=TEMPLATES_DIR, static_folder=STATICFILES_DIR)  # 创建一个蓝图对象，设置别名，模板文件地址，静态文件地址


@admin.context_processor
def magConifg():
    magConifg = {}
    magConifg['username'] = session.get('username')
    return dict(config=magConifg)


from app.admin.index import views
from app.admin.system import views
from app.admin.drive import views