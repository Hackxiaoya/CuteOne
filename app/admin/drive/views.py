# -*- coding:utf-8 -*-
from flask import request, render_template, json
import config
import os, requests, re
from app import MysqlDB
from app import decorators
from app.admin import admin
from ..drive import models
from ..drive import logic
from ..task import models as taskModels
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
            MysqlDB.session.flush()
            MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/drive/drive_del/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def drive_del(id):
    models.drive.deldata(id)
    models.drive_list.deldata_by_drive_id(id)
    return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/drive/disk_list/<int:id>', methods=['GET'])
@admin.route('/drive/disk_list/<int:id>/')  # 设置分页
@decorators.login_require
def disk_list(id):
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
                cache_count = models.mongodb_count(result.id)
                json_data["data"].append(
                    {"id": result.id, "title": result.title, "chief":result.chief, "client_id": result.client_id, "client_secret": result.client_secret, "count": cache_count, "update_time":str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        data = models.drive.find_by_id(id)
        return render_template('admin/drive/disk_list.html', top_nav='drive', activity_nav='list', data=data)


@admin.route('/drive/disk_edit/<int:drive_id>/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def disk_edit(drive_id, id):
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
        return render_template('admin/drive/disk_edit.html', top_nav='drive', activity_nav='edit', data=result)
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
            role = models.drive_list(title=title, drive_id=drive_id, client_id=client_id, client_secret=client_secret, token=token, chief=chief)
            MysqlDB.session.add(role)
            MysqlDB.session.flush()
            MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/drive/file_uploads_big/<int:drive_id>', methods=['GET']) # 大文件上传
@admin.route('/drive/file_uploads_big/<int:drive_id>/', methods=['GET'])
@decorators.login_require
def file_uploads_big(drive_id):
    path = request.args.get('path')
    return render_template('admin/drive/file_uploads_big.html', top_nav='drive', activity_nav='file_uploads', drive_id=drive_id, path=path)

@admin.route('/drive/file_uploads_small/<int:drive_id>', methods=['GET']) # 小文件上传
@admin.route('/drive/file_uploads_small/<int:drive_id>/', methods=['GET'])
@decorators.login_require
def file_uploads_small(drive_id):
    path = request.args.get('path')
    return render_template('admin/drive/file_uploads_small.html', top_nav='drive', activity_nav='file_uploads', drive_id=drive_id, path=path)



@admin.route('/drive/file_uploads', methods=['POST'])
@decorators.login_require
def file_uploads():
    md5value = request.form['md5value']
    chunk = request.form['chunk']
    file = request.files['file']
    file_path = os.getcwd()+"/temp_uploads/"+ md5value
    isExists = os.path.exists(file_path)
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(file_path)
        file.save(file_path + "/" + chunk)
    return json.dumps({})


@admin.route('/drive/file_uploads_check', methods=['GET', 'POST'])
@decorators.login_require
def file_uploads_check():
    md5 = request.form['md5']
    # 通过MD5唯一标识找到缓存文件
    file_path = os.getcwd()+"/temp_uploads/" + md5
    if os.path.exists(file_path):
        block_info = os.listdir(file_path)
        return json.dumps({'block_info': block_info})
    else:
        return json.dumps({})


@admin.route('/drive/file_uploads_success', methods=['GET', 'POST'])
@decorators.login_require
def file_uploads_success():
    drive_id = request.form['drive_id']
    path = request.form['path']
    md5 = request.form['md5']
    fileName = request.form['fileName']
    target_filename = os.getcwd()+"/temp_uploads/" + md5    # 获取上传文件的文件名
    ok_file = os.getcwd()+"/temp_uploads/" + drive_id + "/" + fileName
    if not os.path.exists(os.getcwd()+"/temp_uploads/" + drive_id):
        # 如果不存在则创建目录
        os.makedirs(os.getcwd()+"/temp_uploads/" + drive_id)
    chunk = 0
    with open(ok_file, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = target_filename + "/" + str(chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片
    if os.path.exists(target_filename):
        os.rmdir(target_filename)   # 删除文件夹

    # 初始化role 并插入数据库
    role = taskModels.task(drive_id=drive_id, file_name=fileName,path=path, type='uploads', status=0)
    MysqlDB.session.add(role)
    MysqlDB.session.flush()
    MysqlDB.session.commit()
    # 推送到上传任务
    logic.pull_uploads(role.id, drive_id, fileName, path)
    return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/drive/disk_del/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def disk_del(id):
    models.drive_list.deldata_by_id(id)
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
    drive_id = models.drive_list.find_by_id(id).drive_id
    uploads_path = request.args.get('path')
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
    return render_template('admin/drive/files.html', top_nav='drive', activity_nav='edit', id=id, current_url=current_url, drive_id=drive_id, uploads_path=uploads_path, data=data)


@admin.route('/drive/folder_create', methods=['POST'])
@decorators.login_require
def folder_create():
    id = request.form['id']
    path = request.form['path']
    fileName = request.form['fileName']
    path = re.findall('\?path=(.*?)', path)[0]
    logic.folder_create(id, path, fileName)
    return json.dumps({"code": 0, "msg": "成功！"})


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