# -*- coding:utf-8 -*-
from flask import Blueprint, session
from .menu import models as menuModels

admin = Blueprint('admin', __name__)  # 创建一个蓝图对象，设置别名

@admin.context_processor
def menu_list():
    data = menuModels.menu.all(1)
    menu_list = []
    for item in data:
        if item.pid is None:
            menu_list.append({
                "title": item.title,
                "id": item.id,
                "type_name": item.type_name,
                "top_nav": item.top_nav,
                "activity_nav": item.activity_nav,
                "children": []
            })
        else:
            for v in menu_list:
                if item.pid == v["id"]:
                    v["children"].append({
                        "title": item.title,
                        "url": item.url,
                        "top_nav": item.top_nav,
                        "activity_nav": item.activity_nav
                    })
    return dict(menu_list=menu_list)


@admin.context_processor
def magConifg():
    magConifg = {}
    magConifg['username'] = session.get('username')
    return dict(config=magConifg)



from .index import views
from .menu import views
from .socket import views
from .system import views
from .drive import views
from .author import views
from .task import views
from .syn import views
from .users import views
from .model import views
from .files import views
