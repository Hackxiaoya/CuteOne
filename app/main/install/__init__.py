# -*- coding:utf-8 -*-
from flask import Blueprint


index = Blueprint('install', __name__)  # 创建一个蓝图对象，设置别名

from . import views