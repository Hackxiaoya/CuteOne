# -*- coding:utf-8 -*-
from flask import request, render_template, json
from app import db
from app.admin import admin
from ..drive import models


@admin.route('/drive/list', methods=['GET'])
@admin.route('/drive/list/')  # 设置分页
def list():
    if request.args.get('page'):
        data_list = models.drive.all()
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                json_data["data"].append(
                    {"id": result.id, "title": result.title, "description": result.description,
                     "client_id": result.client_id, "client_secret": result.client_secret, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/drive/list.html', top_nav='drive', activity_nav='list')


@admin.route('/drive/detail/<int:id>')
def detail(id):
    data = {
        'id': '1'
        , 'ip': '192.168.1.146'
        , 'title': '客厅'
        , 'command': '城市-0'
    }
    return render_template('admin/drive/detail.html', top_nav='drive', activity_nav='detail', data=data)


@admin.route('/drive/edit/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
def edit(id):
    if request.method == 'GET':
        if id:
            data_list = models.drive.find_by_id(id)
            result = {}
            result["id"] = data_list.id
            result["title"] = data_list.title
            result["description"] = data_list.description
            result["client_id"] = data_list.client_id
            result["client_secret"] = data_list.client_secret
        else:
            result = {
                'id': '0'
                , 'title': ''
                , 'description': ''
                , 'client_id': ''
                , 'client_secret': ''
            }
        return render_template('admin/drive/edit.html', top_nav='drive', activity_nav='edit', data=result)
    else:
        id = request.form['id']
        title = request.form['title']
        description = request.form['description']
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        if id != '0':
            models.drive.update({"id": id, "title": title, "description": description, "client_id": client_id, "client_secret": client_secret})
        else:
            # 初始化role 并插入数据库
            role = models.drive(title=title, description=description, client_id=client_id, client_secret=client_secret)
            db.session.add(role)
            db.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})