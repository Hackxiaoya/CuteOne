# -*- coding:utf-8 -*-
from flask import render_template, request, json
from app import MysqlDB
from app.admin import admin
from ..menu import models
from app import common


@admin.route('/menu/in_menu_list', methods=['GET'])
@admin.route('/menu/in_menu_list/')  # 设置分页
@common.login_require
def in_menu_list():
    if request.args.get('page'):
        data_list = models.menu.all(0, 1, 2)
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                if result.type == 0:
                    result.type = "<span class='layui-btn layui-btn-normal layui-btn-xs'>自定义</span>"
                elif result.type == 1:
                    result.type = "<span class='layui-btn layui-btn-normal layui-btn-xs'>驱动</span>"
                elif result.type == 2:
                    result.type = "<span class='layui-btn layui-btn-primary layui-btn-xs'>模型</span>"
                else:
                    result.type = "<span class='layui-btn layui-btn-primary layui-btn-xs'>未知</span>"
                if result.activate == 1:
                    result.activate = "<span class='layui-btn layui-btn-normal layui-btn-xs'>是</span>"
                else:
                    result.activate = "<span class='layui-btn layui-btn-primary layui-btn-xs'>否</span>"
                if result.status == 1:
                    result.status = "<span class='layui-btn layui-btn-normal layui-btn-xs'>是</span>"
                else:
                    result.status = "<span class='layui-btn layui-btn-primary layui-btn-xs'>否</span>"
                json_data["data"].append(
                    {"id": result.id, "pid": result.pid, "title": result.title, "type": result.type, "url": result.url, "sort":result.sort, "activate":result.activate, "status":result.status, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/menu/in_menu_list.html', top_nav='menu', activity_nav='in_menu_list')


@admin.route('/menu/out_menu_list', methods=['GET'])
@admin.route('/menu/out_menu_list/')  # 设置分页
@common.login_require
def out_menu_list():
    if request.args.get('page'):
        data_list = models.menu.all(1)
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                if result.type == 0:
                    result.type = "<span class='layui-btn layui-btn-normal layui-btn-xs'>自定义</span>"
                elif result.type == 1:
                    result.type = "<span class='layui-btn layui-btn-normal layui-btn-xs'>驱动</span>"
                elif result.type == 2:
                    result.type = "<span class='layui-btn layui-btn-primary layui-btn-xs'>模型</span>"
                else:
                    result.type = "<span class='layui-btn layui-btn-primary layui-btn-xs'>未知</span>"
                if result.activate == 1:
                    result.activate = "<span class='layui-btn layui-btn-normal layui-btn-xs'>是</span>"
                else:
                    result.activate = "<span class='layui-btn layui-btn-primary layui-btn-xs'>否</span>"
                if result.status == 1:
                    result.status = "<span class='layui-btn layui-btn-normal layui-btn-xs'>是</span>"
                else:
                    result.status = "<span class='layui-btn layui-btn-primary layui-btn-xs'>否</span>"
                json_data["data"].append(
                    {"id": result.id, "pid": result.pid, "title": result.title, "type": result.type, "url": result.url, "sort":result.sort, "activate":result.activate, "status":result.status, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/menu/out_menu_list.html', top_nav='menu', activity_nav='out_menu_list')


@admin.route('/menu/in_edit/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@common.login_require
def in_menu_edit(id):
    if request.method == 'GET':
        if id:
            data_list = models.menu.find_by_id(id)
            result = {}
            result["id"] = data_list.id
            result["title"] = data_list.title
            result["url"] = data_list.url
            result["type"] = data_list.type
            result["activate"] = data_list.activate
            result["sort"] = data_list.sort
            result["status"] = data_list.status
        else:
            result = {
                'id': '0'
                , 'title': ''
                , 'url': ''
                , 'type': 0
                , 'activate': 0
                , 'sort': 0
                , 'status': 1
            }
        return render_template('admin/menu/in_edit.html', top_nav='menu', activity_nav='edit', data=result)
    else:
        id = request.form['id']
        title = request.form['title']
        url = request.form['url']
        type = request.form['type']
        if "activate" in request.form.keys():
            activate = 1
        else:
            activate = 0
        if "status" in request.form.keys():
            status = 1
        else:
            status = 0
        sort = request.form['sort']
        if id != '0':
            models.menu.update({"id": id, "title": title, "type":type, "activate": activate, "url":url, "sort": sort, "status": status})
        else:
            # 初始化role 并插入数据库
            role = models.menu(title=title, type=type, url=url, activate=activate, postion=0, sort=sort, status=status)
            MysqlDB.session.add(role)
            MysqlDB.session.flush()
            MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/menu/out_edit/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@common.login_require
def out_menu_edit(id):
    if request.method == 'GET':
        if id:
            data_list = models.menu.find_by_id(id)
            result = {}
            result["id"] = data_list.id
            result["title"] = data_list.title
            result["url"] = data_list.url
            result["activate"] = data_list.activate
            result["sort"] = data_list.sort
            result["status"] = data_list.status
        else:
            result = {
                'id': '0'
                , 'title': ''
                , 'url': ''
                , 'activate': 0
                , 'sort': 0
                , 'status': 1
            }
        return render_template('admin/menu/out_edit.html', top_nav='menu', activity_nav='edit', data=result)
    else:
        id = request.form['id']
        title = request.form['title']
        url = request.form['url']
        type = request.form['type']
        if "activate" in request.form.keys():
            activate = 1
        else:
            activate = 0
        if "status" in request.form.keys():
            status = 1
        else:
            status = 0
        sort = request.form['sort']
        if id != '0':
            models.menu.update({"id": id, "title": title, "type":type, "url":url, "activate": activate, "sort": sort, "status": status})
        else:
            # 初始化role 并插入数据库
            role = models.menu(title=title, type=type, url=url, activate=activate, postion=1, sort=sort, status=status)
            MysqlDB.session.add(role)
            MysqlDB.session.flush()
            MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/menu/del/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@common.login_require
def menu_del(id):
    models.menu.deldata(id)
    return json.dumps({"code": 0, "msg": "完成！"})

