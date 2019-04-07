# -*- coding:utf-8 -*-
from flask import Blueprint, session

admin = Blueprint('admin', __name__)  # 创建一个蓝图对象，设置别名


@admin.context_processor
def magConifg():
    magConifg = {}
    magConifg['username'] = session.get('username')
    return dict(config=magConifg)


from .index import views
from .socket import views
from .system import views
from .drive import views
from .author import views
from .task import views
from .syn import views
from .users import views
from .files import views