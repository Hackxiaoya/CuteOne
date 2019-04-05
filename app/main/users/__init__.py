# -*- coding:utf-8 -*-
from flask import Blueprint


users = Blueprint('users', __name__)  # 创建一个蓝图对象，设置别名

from . import views  # 这里导入是为了在解释时，蓝图能加载到views文件中的路由数据