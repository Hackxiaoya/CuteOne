# -*- coding:utf-8 -*-
from flask import request, render_template, json
from app import MysqlDB
import config
from .. import admin
from . import models
from . import logic
from ..drive import models as driveModels
from app import common
from app import decorators



@admin.route('/task/list', methods=['GET'])
@admin.route('/task/list/')
@decorators.login_require
def task_list():
    if request.args.get('page'):
        data_list = models.task.all()
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                drive_name = driveModels.drive.find_by_id(result.drive_id).title
                if result.status == "0":
                    istask = logic.isPullUploads(result.id)
                    if istask:
                        result.status = "<button class='layui-btn layui-btn-xs'>进行中</button>"
                    else:
                        result.status = "<button class='layui-btn layui-btn-primary layui-btn-xs'>中断</button>"
                elif result.status == "1":
                    result.status = "<button class='layui-btn layui-btn-normal layui-btn-xs'>完成</button>"
                else:
                    result.status = "进行中"
                json_data["data"].append(
                    {"id": result.id, "drive_name": drive_name, "path": result.path, "file_name":result.file_name, "type": result.type, "status":result.status, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/task/list.html', top_nav='task', activity_nav='list')


# @admin.route('/task/edit/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
# @decorators.login_require
# def task_edit(id):
#     if request.method == 'GET':
#         drive_list = driveModels.drive.all()
#         drive_data = []
#         if drive_list:
#             for i in drive_list:
#                 drive_data.append({"drive_id": i.id, "drive_title": i.title})
#         if id:
#             data_list = models.task.find_by_id(id)
#             result = {}
#             result["id"] = data_list.id
#             result["title"] = data_list.title
#             result["drive_id"] = data_list.drive_id
#             result["path"] = data_list.path
#             result["password"] = data_list.password
#         else:
#             result = {
#                 'id': '0'
#                 , 'title': ''
#                 , 'drive_id': ''
#                 , 'path': ''
#                 , 'password': 0
#             }
#         return render_template('admin/author/edit.html', top_nav='author', activity_nav='edit', drive_list=drive_data, data=result)
#     else:
#         id = request.form['id']
#         title = request.form['title']
#         drive_id = request.form['drive_id']
#         path = request.form['path']
#         password = request.form['password']
#         if id != '0':
#             models.authrule.update({"id": id, "title": title, "drive_id": drive_id, "path": path, "password": password})
#         else:
#             # 初始化role 并插入数据库
#             role = models.authrule(title=title, drive_id=drive_id, path=path, password=password)
#             MysqlDB.session.add(role)
#             MysqlDB.session.flush()
#             MysqlDB.session.commit()
#         return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/task/del/<int:id>', methods=['GET', 'POST'])  # 删除
@decorators.login_require
def task_del(id):
    models.task.deldata(id)
    return json.dumps({"code": 0, "msg": "完成！"})
