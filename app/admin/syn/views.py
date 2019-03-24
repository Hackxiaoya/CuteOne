# -*- coding:utf-8 -*-
from flask import request, render_template, json
from app import MysqlDB
from .. import admin
from . import models
from ..drive import models as driveModels
from app import decorators



@admin.route('/syn/syn_start/<int:drive_id>', methods=['GET', 'POST'])  # 主从同步
@decorators.login_require
def syn_start(drive_id):
    disk_list = driveModels.drive_list.find_by_drive_id(drive_id)
    
    return json.dumps({"code": 0, "msg": "完成！"})
