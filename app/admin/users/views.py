# -*- coding:utf-8 -*-
import time, os, hashlib, random
from flask import request, render_template, json
from app import MysqlDB
from app import decorators
from .. import admin
from . import models
from ..author import models as authorModels
from app import common
from ..system import models as systemModels



@admin.route('/users/list', methods=['GET', 'POST'])
@admin.route('/users/list/')  # 设置分页
@decorators.login_require
def users_list():
    if request.args.get('page'):
        data_list = models.users.all()
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                if result.group:
                    group = authorModels.authGroup.find_by_id(result.group).title
                else:
                    group = "普通会员"
                if result.status:
                    status = "<button class='layui-btn layui-btn-normal layui-btn-xs'>正常</button>"
                else:
                    status = "<button class='layui-btn layui-btn-danger layui-btn-xs'>禁用</button>"
                json_data["data"].append(
                    {"id": result.id, "username": result.username, "nickname": result.nickname, "avatar":result.avatar, "score":result.score, "group":group, "status":status, "last_login_time": str(result.last_login_time), "reg_time": str(result.reg_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/users/list.html', top_nav='users', activity_nav='list')


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])  # 新增/编辑
@decorators.login_require
def users_edit(id):
    if request.method == 'GET':
        group_list = authorModels.authGroup.all()
        group_list_data = []
        for item in group_list:
            group_list_data.append({"id":item.id, "title":item.title})
        if id:
            data_list = models.users.find_by_id(id)
            result = {}
            result["id"] = data_list.id
            result["username"] = data_list.username
            result["password"] = data_list.password
            result["nickname"] = data_list.nickname
            result["email"] = data_list.email
            result["description"] = data_list.description
            result["group"] = data_list.group
            result["avatar"] = data_list.avatar
            result["sex"] = data_list.sex
            result["score"] = data_list.score
            result["files_disk_id"] = data_list.files_disk_id
            result["status"] = data_list.status
        else:
            nickname = ["菜刀诗人", "SUONGLO", "你是哪块小饼干呐", "-夕凉_", "散漫的Taco", "奥特曼", "渡尘烟", "知意南风", "绿色橘生", "花胖胖", "侬本多情", "情欲孤独", "麦记花"]
            files_disk_id = '0' if systemModels.config.get_config('files_disk_id') == None else systemModels.config.get_config('files_disk_id').value
            result = {
                'id': '0'
                , 'username': ''
                , 'password': ''
                , 'nickname': random.choice(nickname)
                , 'email': ''
                , 'description': '素面朝天浅笑吟，倾国倾城两相宜.'
                , 'score': 0
                , 'group': 0
                , 'avatar': "/static/uploads/avatar/{}.png".format(random.randint(1, 10))
                , 'sex': 3
                , 'files_disk_id': files_disk_id
                , 'status': 1
            }
        return render_template('admin/users/edit.html', top_nav='users', activity_nav='edit', data=result, group_list=group_list_data)
    else:
        from_data = request.form
        from_data = from_data.to_dict()
        # 是否修改密码
        if from_data['password']:
            from_data['password'] = common.hashPwd(from_data['password'])
        else:
            from_data.pop('password')   # 不修改密码，删除键值
        if "status" in request.form.keys():
            from_data['status'] = 1
        else:
            from_data['status'] = 0
        if id != 0:
            models.users.update(from_data)
            return json.dumps({"code": 0, "msg": "完成！"})
        else:
            checkName = models.users.check_username(from_data['username'])
            if checkName is None:
                # 初始化role 并插入数据库
                role = models.users(
                    username=from_data['username'],
                    password=from_data['password'],
                    nickname=from_data['nickname'],
                    email=from_data['email'],
                    description=from_data['description'],
                    avatar=from_data['avatar'],
                    sex=from_data['sex'],
                    login_num=0,
                    score=from_data['score'],
                    group=from_data['group'],
                    status=from_data['status'],
                    register_ip='127.0.0.1',
                    birthday='0001-01-01 00:00:00',
                    reg_time=time.strftime('%Y-%m-%d %H:%M:%S'),
                    update_time=time.strftime('%Y-%m-%d %H:%M:%S')
                )
                MysqlDB.session.add(role)
                MysqlDB.session.flush()
                MysqlDB.session.commit()
                return json.dumps({"code": 0, "msg": "完成！"})
            else:
                return json.dumps({"code": 1, "msg": "用户名已存在！"})


@admin.route('/users/users_del/<int:id>', methods=['GET', 'POST'])
@decorators.login_require
def users_del(id):
    models.users.deldata(id)
    return json.dumps({"code": 0, "msg": "完成！"})


@admin.route('/users/upload', methods=['POST'])
@decorators.login_require
def upload_avatar():
    file = request.files.get('file')
    fileName = hashlib.sha1(file.read()).hexdigest()
    file.seek(0)
    file_path = "/app/static/uploads/avatar/{}.{}".format(os.getcwd(), fileName, file.filename.rsplit('.',1)[1])
    src_path = "/static/uploads/avatar/{}.{}".format(fileName, file.filename.rsplit('.',1)[1])
    file.save(os.getcwd()+file_path)
    return json.dumps({"code": 0, "msg": "", "data": {"src": src_path}})


@admin.route('/users/funds_list', methods=['GET', 'POST'])  # 主从同步
@admin.route('/users/funds_list/')  # 设置分页
@decorators.login_require
def funds_list():
    if request.args.get('page'):
        data_list = models.funds.all()
        json_data = {"code": 0, "msg": "", "count": 0, "data": []}
        if data_list:
            for result in data_list:
                json_data["count"] = json_data["count"]+1
                users_info = models.users.find_by_id(result.uid)
                username = users_info.username
                nickname = users_info.nickname
                if result.status:
                    status = "<button class='layui-btn layui-btn-normal layui-btn-xs'>完成</button>"
                else:
                    status = "<button class='layui-btn layui-btn-danger layui-btn-xs'>未完成</button>"
                json_data["data"].append(
                    {"id": result.id, "username": username, "nickname": nickname, "content":result.content, "status":status, "update_time": str(result.update_time), "create_time": str(result.create_time)})
        return json.dumps(json_data)
    else:
        return render_template('admin/users/funds_list.html', top_nav='users', activity_nav='funds_list')