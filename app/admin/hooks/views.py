# -*- coding:utf-8 -*-
from flask import request, render_template, json
from app import MysqlDB
from .. import admin
from . import models
from ..model import models as modelModels
from ..plugin import models as pluginModels
from app import decorators


@admin.route('/hooks/list', methods=['GET'])
@admin.route('/hooks/list/')
@decorators.login_require
def hooks_list():
    if request.args.get('page'):
        data_list = models.hooks.all()
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                if result.type == 0:
                    result.type = "<button class='layui-btn layui-btn-xs'>模型</button>"
                    result.name = modelModels.model.find_by_name(result.source).title
                else:
                    result.type = "<button class='layui-btn layui-btn-xs'>插件</button>"
                    result.name = pluginModels.plugin.find_by_name(result.source).title
                json_data["data"].append(
                    {"id": result.id, "title": result.title, "description": result.description, "type": result.type, "name": result.name, "status":result.status, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/hooks/list.html', top_nav='hooks', activity_nav='list')


@admin.route('/hooks/edit/<int:id>', methods=['GET', 'POST'])
@decorators.login_require
def hooks_edit(id):
    if request.method == 'GET':
        if id:
            data_list = models.hooks.find_by_id(id)
            result = {}
            result["id"] = data_list.id
            result["title"] = data_list.title
            result["description"] = data_list.description
            result["type"] = data_list.type
            result["method"] = data_list.method
        else:
            result = {
                'id': '0'
                , 'title': ''
                , 'description': ''
            }
        return render_template('admin/hooks/edit.html', top_nav='hooks', activity_nav='edit', data=result)
    else:
        id = request.form['id']
        title = request.form['title']
        description = request.form['description']
        type = request.form['type']
        method = request.form['method']
        if id != '0':
            models.hooks.update({"id": id, "title": title, "description": description, "type": type, "method": method})
        # else:
        #     # 初始化role 并插入数据库
        #     role = models.task(title=title, description=description, path=path, type=type)
        #     MysqlDB.session.add(role)
        #     MysqlDB.session.flush()
        #     MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/hooks/hooksdel/<int:id>', methods=['GET', 'POST'])  # 删除
@decorators.login_require
def hooks_del(id):
    models.hooks.deldata(id)
    return json.dumps({"code": 0, "msg": "完成！"})