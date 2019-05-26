# -*- coding:utf-8 -*-
import importlib
from flask import render_template
from app.admin.system import models as systemModels
from app.main import index
from app.admin.menu import models as menuModels
from ..indexs import drive as driveViews
import config
THEMES = 'themes/'+ config.THEMES +'/'

@index.before_request
def toggle_web_site():
    toggle_web_site = systemModels.config.get_config("toggle_web_site")
    if toggle_web_site == "0":
        return render_template('toggle/index_1.html')


@index.context_processor
def drive_list():
    menu_list = menuModels.menu.all(0, 1)
    return dict(menu_list=menu_list)


# 错误提示回调
def error_tip(value):
    return render_template('error/error.html', data=value), 500



@index.route('/')
def _index():
    active = menuModels.menu.find_by_index()
    if active:
        if active.type == 1:
            indexModel = driveViews.drive(active.type_name)
        elif active.type == 2:
            model_name = importlib.import_module("app.model." + active.type_name + ".controller.views")  # 相当于from app.model.movie.controller import views
            indexModel = getattr(model_name, active.type_name+"_index")()
        return indexModel
    else:
        return error_tip("没有设置默认首页")

