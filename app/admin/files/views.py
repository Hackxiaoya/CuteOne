# -*- coding:utf-8 -*-
from flask import request, render_template, json
import requests
import config
from app import MysqlDB
from .. import admin
from . import models
from . import logic
from app.admin.files import models as filesModels
from app import decorators, common



@admin.route('/files/files_disk_list', methods=['GET'])
@admin.route('/files/files_disk_list/')
@decorators.login_require
def files_disk_list():
    if request.args.get('page'):
        data_list = models.filesDisk.all()
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"] + 1
                cache_count = "0"
                json_data["data"].append(
                    {"id": result.id, "title": result.title, "description": result.description, "client_id": result.client_id,
                     "client_secret": result.client_secret, "count": cache_count,
                     "update_time": str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/files/files_disk_list.html', top_nav='files', activity_nav='files_disk_list')


@admin.route('/files/files_disk_edit/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def files_disk_edit(id):
    if request.method == 'GET':
        if id:
            data_list = models.filesDisk.find_by_id(id)
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
                , 'code': ''
            }
        return render_template('admin/files/files_disk_edit.html', top_nav='files', activity_nav='edit', data=result)
    else:
        id = request.form['id']
        title = request.form['title']
        description = request.form['description']
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        code = request.form['code']
        if id != '0':
            models.filesDisk.update({"id": id, "title": title, "client_id": client_id, "client_secret": client_secret, "description":description})
        else:
            url = config.BaseAuthUrl + '/common/oauth2/v2.0/token'
            redirect_url = "http://127.0.0.1/"
            AuthData = 'client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}&grant_type=authorization_code'
            data = AuthData.format(client_id=client_id, redirect_uri=redirect_url, client_secret=client_secret, code=code)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'ISV|CuteOne|CuteOne/1.0'
            }
            res = requests.post(url,data=data,headers=headers)
            token = json.dumps(res.text)

            # 初始化role 并插入数据库
            role = models.filesDisk(title=title, description=description, client_id=client_id, client_secret=client_secret, token=token)
            MysqlDB.session.add(role)
            MysqlDB.session.flush()
            MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/files/files_disk_del/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def files_disk_del(id):
    models.filesDisk.deldata(id)
    return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/files/files_disk_files/<int:id>/', methods=['GET'])
@decorators.login_require
def files_disk_files(id):
    uploads_path = request.args.get('path')
    if request.args.get('path'):
        path = request.args.get("path")
        current_url = '/admin/files/files_disk_files/' + str(id) + '/?path=' + path
    else:
        path = ''
        current_url = '/admin/files/files_disk_files/' + str(id) + '/?path='
    data = logic.get_one_file_list(id, path)
    for i in data["data"]["value"]:
        i["lastModifiedDateTime"] = common.utc_to_local(i["lastModifiedDateTime"])
        i["size"] = common.size_cov(i["size"])
    data = data["data"]["value"]
    return render_template('admin/files/files_disk_files.html', top_nav='files', activity_nav='edit', id=id, current_url=current_url, data=data)



@admin.route('/files/files_manage/', methods=['GET'])
@decorators.login_require
def files_manage(id):
    result = filesModels.files.find_by_id()
    print(1)