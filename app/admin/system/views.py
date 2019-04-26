# -*- coding:utf-8 -*-
import os
from flask import request, render_template, json
import config
from .. import admin
from ..system import models
from ..system import logic
from app import common
from app import decorators



@admin.route('/system/restart', methods=['GET', 'POST'])  # restart
@decorators.login_require
def restart():
    common.restart()
    return json.dumps({"code": 0, "msg": "成功！"})


@admin.route('/system/manage', methods=['GET', 'POST'])  # 管理
@decorators.login_require
def manage():
    info = common.SystemInfo
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
        # 用户模块关闭/开启
        if 'is_users' in from_data.keys():
            from_data['is_users'] = 1
        else:
            from_data['is_users'] = 0
        for i in from_data:
            models.config.update({"name": i, "value": from_data[i]})
        return json.dumps({"code": 0, "msg": "保存成功！"})


@admin.route('/system/front', methods=['GET', 'POST'])
@decorators.login_require
def front():
    if request.method == 'GET':
        data = models.config.all()
        # print(data)
        result = data
        return render_template('admin/system/front.html', top_nav='system', activity_nav='front', data=result)
    else:
        from_data = request.form
        from_data = from_data.to_dict()
        # 搜索类型关闭/开启
        if 'search_type' in from_data.keys():
            from_data['search_type'] = 1
        else:
            from_data['search_type'] = 0
        # 音乐播放关闭/开启
        if 'is_music' in from_data.keys():
            from_data['is_music'] = 1
        else:
            from_data['is_music'] = 0
        # 用户上传关闭/开启
        if 'files_uploads' in from_data.keys():
            from_data['files_uploads'] = 1
        else:
            from_data['files_uploads'] = 0
        for i in from_data:
            models.config.update({"name": i, "value": from_data[i]})
        return json.dumps({"code": 0, "msg": "保存成功！"})


@admin.route('/system/upload_logo', methods=['POST'])
@decorators.login_require
def upload_logo():
    img = request.files.get('file')
    file_path = os.getcwd()+"/app/static/uploads/logo.png"
    img.save(file_path)
    url = "/static/uploads/logo.png"
    return json.dumps({"code": 0, "msg": "", "data": {"src": url}})


@admin.route('/system/upload', methods=['POST'])
@decorators.login_require
def upload_bg():
    img = request.files.get('file')
    file_path = os.getcwd()+"/app/static/uploads/site_background.jpg"
    img.save(file_path)
    url = "/static/uploads/site_background.jpg"
    return json.dumps({"code": 0, "msg": "", "data": {"src": url}})


@admin.route('/system/themes', methods=['GET', 'POST'])
@decorators.login_require
def themes():
    if request.method == 'GET':
        themes_list = logic.get_themes_list()
        return render_template('admin/system/themes.html', top_nav='system', activity_nav='themes', data=themes_list)
    else:
        name = request.form['name']
        logic.modify_themes_config(name)
        return json.dumps({"code": 0, "msg": "保存成功！"})