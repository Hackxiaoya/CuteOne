# -*- coding:utf-8 -*-
import sys, os, time
from flask import request, render_template, json
import config
from .. import admin
from ..system import models
from app import common
from app import decorators



@admin.route('/system/manage')  # 管理
@decorators.login_require
def manage():  # 执行的方法
    info = config.SystemInfo
    result = {
        "name": info["name"],
        "versionType": info["versionType"],
        "versions": info["versions"]
    }
    return render_template('admin/system/manage.html', top_nav='system', activity_nav='manage', data=result)


@admin.route('/system/setting', methods=['GET', 'POST'])
@decorators.login_require
def setting():
    if request.method == 'GET':
        data = models.config.all()
        # print(data)
        result = data
        return render_template('admin/system/setting.html', top_nav='system', activity_nav='setting', data=result)
    else:
        from_data = request.form
        from_data = from_data.to_dict()
        print(from_data)
        # 是否修改管理员密码
        if from_data['password']:
            from_data['password'] = common.hashPwd(from_data['password'])
        else:
            from_data.pop('password')   # 不修改密码，删除键值
        # 站点关闭/开启
        if 'toggle_web_site' in from_data.keys():
            from_data['toggle_web_site'] = 1
        else:
            from_data['toggle_web_site'] = 0
        for i in from_data:
            models.config.update({"name": i, "value": from_data[i]})
        return json.dumps({"code": 0, "msg": "保存成功！"})