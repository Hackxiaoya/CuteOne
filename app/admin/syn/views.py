# -*- coding:utf-8 -*-
from flask import request, render_template, json
from app import MysqlDB
from .. import admin
from . import models
from ..drive import models as driveModels
from app import decorators



@admin.route('/syn/list', methods=['GET', 'POST'])  # 主从同步
@admin.route('/syn/list/')  # 设置分页
# @decorators.login_require
def syn_list():
    return render_template('admin/syn/list.html', activity_nav='syn', data='')
