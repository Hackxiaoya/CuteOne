# -*- coding:utf-8 -*-
import importlib
from flask import Blueprint, session
try:
    from app.admin.model import models as modelModels
    from app.admin.system import models as systemModels
except Exception as e:
    pass

index = Blueprint('/', __name__)  # 创建一个蓝图对象，设置别名


# 基本配置
# @index.context_processor
# def webconfig():
#     try:
#         webconfig = systemModels.config.all()
#         webconfig.pop('username')
#         webconfig.pop('password')
#         return dict(webconfig=webconfig)
#     except:
#         pass



from .indexs import views
try:
    model_list = modelModels.model.all()
    if model_list:
        for item in model_list:
            importlib.import_module("app.model."+item.name+".controller.views")  # 相当于from app.model.movie.admin import views
except Exception as e:
    pass