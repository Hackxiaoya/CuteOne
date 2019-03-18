# -*- coding:utf-8 -*-
from flask import redirect, request, render_template, json
import config
import requests, time, datetime
from app import MysqlDB
from app import decorators
from app.admin import admin
from ..drive import models
from ..drive import logic
from app import common


@admin.route('/drive/list', methods=['GET'])
@admin.route('/drive/list/')  # 设置分页
@decorators.login_require
def list():
    isRunning = common.isRunning("cuteTask")    # 检测是否有更新任务
    if request.args.get('page'):
        data_list = models.drive.all()
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                drive_number = len(models.drive_list.all(result.id))
                json_data["data"].append(
                    {"id": result.id, "title": result.title, "description": result.description, "drive_number":drive_number, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/drive/list.html', top_nav='drive', activity_nav='list', isRunning=isRunning)


@admin.route('/drive/edit/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def edit(id):
    if request.method == 'GET':
        if id:
            data_list = models.drive.find_by_id(id)
            result = {}
            result["id"] = data_list.id
            result["title"] = data_list.title
            result["description"] = data_list.description
            result["activate"] = data_list.activate
            result["sort"] = data_list.sort
        else:
            result = {
                'id': '0'
                , 'title': ''
                , 'description': ''
                , 'activate': 0
                , 'sort': 0
            }
        return render_template('admin/drive/edit.html', top_nav='drive', activity_nav='edit', data=result)
    else:
        id = request.form['id']
        title = request.form['title']
        description = request.form['description']
        if "activate" in request.form.keys():
            activate = 1
        else:
            activate = 0
        sort = request.form['sort']
        if id != '0':
            models.drive.update({"id": id, "title": title, "description": description, "activate": activate, "sort": sort})
        else:
            # 初始化role 并插入数据库
            role = models.drive(title=title, description=description, activate=activate, sort=sort)
            MysqlDB.session.add(role)
            MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})






@admin.route('/drive/drive_list/<int:id>', methods=['GET'])
@admin.route('/drive/drive_list/<int:id>/')  # 设置分页
@decorators.login_require
def drive_list(id):
    if request.args.get('page'):
        data_list = models.drive_list.all(id)
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                if result.chief == "1":
                    result.chief = "主盘"
                else:
                    result.chief = "从盘"
                json_data["data"].append(
                    {"id": result.id, "title": result.title, "chief":result.chief, "client_id": result.client_id, "client_secret": result.client_secret, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        data = models.drive.find_by_id(id)
        return render_template('admin/drive/drive_list.html', top_nav='drive', activity_nav='list', data=data)


@admin.route('/drive/drive_edit/<int:drive_id>/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def drive_edit(drive_id, id):
    if request.method == 'GET':
        if id:
            data_list = models.drive_list.find_by_id(id)
            result = {}
            result["drive_id"] = data_list.drive_id
            result["id"] = data_list.id
            result["title"] = data_list.title
            result["client_id"] = data_list.client_id
            result["client_secret"] = data_list.client_secret
            result["chief"] = data_list.chief
        else:
            result = {
                'drive_id': drive_id
                ,'id': '0'
                , 'title': ''
                , 'client_id': ''
                , 'client_secret': ''
                , 'code': ''
                , 'chief': '0'
            }
        return render_template('admin/drive/drive_edit.html', top_nav='drive', activity_nav='edit', data=result)
    else:
        drive_id = request.form['drive_id']
        id = request.form['id']
        title = request.form['title']
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        code = request.form['code']
        chief = request.form['chief']
        if id != '0':
            models.drive_list.update({"id": id, "title": title, "client_id": client_id, "client_secret": client_secret, "chief":chief})
        else:
            url = config.BaseAuthUrl + '/common/oauth2/v2.0/token'
            redirect_url = common.get_web_site()
            AuthData = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}&grant_type=authorization_code'
            data = AuthData.format(client_id=client_id, redirect_uri=redirect_url, client_secret=client_secret, code=code)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'ISV|CuteOne|CuteOne/1.0'
            }
            res = requests.post(url,data=data,headers=headers)
            token = json.dumps(res.text)

            # 初始化role 并插入数据库
            role = models.drive_list(title=title, drive_id=drive_id, client_id=client_id, client_secret=client_secret, token=token, chief=chief)
            MysqlDB.session.add(role)
            MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/drive/update_cache', methods=['POST'])  # 更新MongoDB缓存
@decorators.login_require
def update_cache():
    drive_id = request.form['id']
    type = request.form['type']
    logic.update_cache(drive_id, type)
    return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/drive/files/<int:id>', methods=['GET'])
@admin.route('/drive/files/<int:id>/', methods=['GET'])
@decorators.login_require
def files(id):
    if request.args.get('path'):
        path = request.args.get("path")
        current_url = '/admin/drive/files/' + str(id) + '/?path=' + path
    else:
        path = ''
        current_url = '/admin/drive/files/' + str(id) + '/?path='
    data = logic.get_one_file_list(id, path)
    print(data["data"]["value"])
    for i in data["data"]["value"]:
        i["lastModifiedDateTime"] = common.utc_to_local(i["lastModifiedDateTime"])
        i["size"] = common.size_cov(i["size"])
    data = data["data"]["value"]
    return render_template('admin/drive/files.html', top_nav='drive', activity_nav='edit', id=id, current_url=current_url, data=data)


@admin.route('/drive/rename_files', methods=['POST'])
@decorators.login_require
def rename_files():
    id = request.form['id']
    fileid = request.form['fileid']
    new_name = request.form['new_name']
    logic.rename_files(id, fileid, new_name)
    return json.dumps({"code": 0, "msg": "成功！"})


@admin.route('/drive/delete_files', methods=['POST'])
@decorators.login_require
def delete_files():
    id = request.form['id']
    fileid = request.form['fileid']
    logic.delete_files(id, fileid)
    return json.dumps({"code": 0, "msg": "成功！"})