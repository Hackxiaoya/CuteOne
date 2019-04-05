# -*- coding:utf-8 -*-
from flask import request, render_template, json
from app import MysqlDB
import config
from .. import admin
from ..author import models
from ..drive import models as driveModels
from app import common
from app import decorators
from operator import itemgetter
from itertools import groupby



@admin.route('/author/list', methods=['GET'])
@admin.route('/author/list/')
@decorators.login_require
def author_list():
    if request.args.get('page'):
        data_list = models.authrule.all()
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                dirve_name = driveModels.drive.find_by_id(result.drive_id).title
                json_data["data"].append(
                    {"id": result.id, "title": result.title, "dirve_name": dirve_name, "path": result.path, "password": result.password, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/author/list.html', top_nav='author', activity_nav='list')


@admin.route('/author/edit/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def author_edit(id):
    if request.method == 'GET':
        drive_list = driveModels.drive.all()
        drive_data = []
        if drive_list:
            for i in drive_list:
                drive_data.append({"drive_id": i.id, "drive_title": i.title})
        if id:
            data_list = models.authrule.find_by_id(id)
            result = {}
            result["id"] = data_list.id
            result["title"] = data_list.title
            result["drive_id"] = data_list.drive_id
            result["path"] = data_list.path
            result["password"] = data_list.password
            result["login_hide"] = data_list.login_hide
        else:
            result = {
                'id': '0'
                , 'title': ''
                , 'drive_id': ''
                , 'path': ''
                , 'password': 0
                , 'login_hide': 0
            }
        return render_template('admin/author/edit.html', top_nav='author', activity_nav='edit', drive_list=drive_data, data=result)
    else:
        id = request.form['id']
        title = request.form['title']
        drive_id = request.form['drive_id']
        path = request.form['path']
        password = request.form['password']
        login_hide = request.form['login_hide']
        if id != '0':
            models.authrule.update({"id": id, "title": title, "drive_id": drive_id, "path": path, "password": password, "login_hide": login_hide})
        else:
            # 初始化role 并插入数据库
            role = models.authrule(title=title, drive_id=drive_id, path=path, password=password, login_hide=login_hide)
            MysqlDB.session.add(role)
            MysqlDB.session.flush()
            MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/author/del/<int:id>', methods=['GET', 'POST'])  # 删除
@decorators.login_require
def author_del(id):
    models.authrule.deldata(id)
    return json.dumps({"code": 0, "msg": "完成！"})



def get_author_list():
    data_list = models.authrule.all()
    data = []
    for item in data_list:
        dirve_name = driveModels.drive.find_by_id(item.drive_id).title
        data.append({
            "id": item.id,
            "drive_name": dirve_name,
            "title": item.title,
            "path": item.path
        })
    data.sort(key=itemgetter('drive_name'))
    lstg = groupby(sorted(data, key=itemgetter('drive_name')), key=itemgetter('drive_name'))
    lstgall = list([(key, list(group)) for key, group in lstg])
    json_data = []
    for ints in lstgall:
        json_data.append({
            "title": ints[0],
            "children": ints[1]
        })
    return json_data


@admin.route('/author/group', methods=['GET'])
@admin.route('/author/group/')
@decorators.login_require
def group_list():
    if request.args.get('page'):
        data_list = models.authGroup.all()
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                json_data["data"].append(
                    {"id": result.id, "title": result.title, "description": result.description, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/author/group.html', top_nav='author', activity_nav='group')


@admin.route('/author/group_edit/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def group_edit(id):
    if request.method == 'GET':
        author_list = get_author_list()
        if id:
            data_list = models.authGroup.find_by_id(id)
            result = {}
            result["id"] = data_list.id
            result["title"] = data_list.title
            result["description"] = data_list.description
            result["auth_group"] = data_list.auth_group
        else:
            result = {
                'id': '0'
                , 'title': ''
                , 'description': ''
                , 'auth_group': ''
            }
        return render_template('admin/author/group_edit.html', top_nav='author', activity_nav='edit', data=result, author_list=author_list)
    else:
        id = request.form['id']
        title = request.form['title']
        description = request.form['description']
        auth_group = request.form['auth_group']
        if id != '0':
            models.authGroup.update({"id": id, "title": title, "description": description, "auth_group": auth_group})
        else:
            # 初始化role 并插入数据库
            role = models.authGroup(title=title, description=description, auth_group=auth_group)
            MysqlDB.session.add(role)
            MysqlDB.session.flush()
            MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/author/group_del/<int:id>', methods=['GET', 'POST'])  # 删除
@decorators.login_require
def group_del(id):
    models.authGroup.deldata(id)
    return json.dumps({"code": 0, "msg": "完成！"})