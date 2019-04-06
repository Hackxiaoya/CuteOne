# -*- coding:utf-8 -*-
import time, json, random, os, hashlib
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from flask_login import login_user, logout_user
from app.admin.users import models as usersModels
from app.admin.author import models as authorModels
from app import MysqlDB
from app.main import index
from ..users import logic
from app import common
import config
THEMES = 'themes/'+ config.THEMES +'/'




@index.route('/users/login', methods=['GET', 'POST'])  # Login
def login():
    if request.method == 'GET':
        return render_template(THEMES + 'users/login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        password = common.hashPwd(password)
        res = usersModels.users.checkpassword(username, password, request.remote_addr)
        if res["code"]:
            model = usersModels.users()  # 实例化一个对象，将查询结果逐一添加给对象的属性
            model.id = res["msg"].id
            model.username = res["msg"].username
            model.avatar = res["msg"].avatar
            model.nickname = res["msg"].nickname
            model.score = res["msg"].score
            if res["msg"].group:
                model.group = authorModels.authGroup.find_by_id(res["msg"].group).title
            else:
                model.group = "普通会员"
            login_user(model)
            return json.dumps({"code": 0, "msg": "登陆成功！"})
        else:
            return json.dumps({"code": 1, "msg": res["msg"]})


@index.route('/users/register', methods=['GET', 'POST'])  # Register
def register():
    username = request.form['username']
    password = request.form['password']
    nickname = request.form['nickname']
    if len(password) < 6:
        return json.dumps({"code": 1, "msg": "密码格式错误"})
    password = common.hashPwd(password)
    res = usersModels.users.check_username(username)
    if res:
        return json.dumps({"code": 1, "msg": "用户名已存在"})
    else:
        # 初始化role 并插入数据库
        role = usersModels.users(
            username = username,
            password = password,
            nickname = nickname,
            email = '',
            description = '',
            avatar = "/static/uploads/avatar/{}.png".format(random.randint(1, 10)),
            sex = 3,
            score = 0,
            group = 0,
            status = 1,
            register_ip = request.remote_addr,
            birthday = '0001-01-01 00:00:00',
            reg_time = time.strftime('%Y-%m-%d %H:%M:%S'),
            update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        )
        MysqlDB.session.add(role)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        return json.dumps({"code": 0, "msg": "注册成功！"})


@index.route("/users/logout")
def logout():
    logout_user()
    return redirect(url_for('/._index'))


@index.route('/users/users_list', methods=['GET', 'POST'])
@index.route('/users/users_list/', methods=['GET', 'POST'])
def users_list():
    page_number = '1' if request.args.get('page') is None else request.args.get('page')
    result = logic.get_users_list(page_number, 12)
    return render_template(THEMES+'users/users_list.html', data=result)


@index.route('/users/personal/<int:id>', methods=['GET', 'POST'])
def personal(id):
    result = usersModels.users.find_by_id(id)
    if result.group == 0:
        result.group = "普通会员"
    else:
        result.group = authorModels.authGroup.find_by_id(result.group).title
    return render_template(THEMES+'users/personal.html', data=result)


@index.route('/users/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'GET':
        if current_user.get_id() is not None:
            result = usersModels.users.find_by_id(current_user.id)
            return render_template(THEMES + 'users/setting.html', data=result)
        else:
            return redirect(url_for('/._index'))
    else:
        if current_user.get_id() is not None:
            from_data = request.form
            from_data = from_data.to_dict()
            from_data['id'] = current_user.id
            if int(from_data['formtype']) == 1:
                from_data.pop('formtype')
                # 是否修改密码
                if from_data['password']:
                    from_data['password'] = common.hashPwd(from_data['password'])
                else:
                    from_data.pop('password')  # 不修改密码，删除键值
                usersModels.users.update(from_data)
                return json.dumps({"code": 0, "msg": "完成！"})
        else:
            return json.dumps({"code": 1, "msg": "未登陆！"})


@index.route('/users/upload', methods=['POST'])
def upload_avatar():
    if current_user.get_id() is not None:
        file = request.files.get('file')
        fileName = hashlib.sha1(file.read()).hexdigest()
        file.seek(0)
        file_path = "/app/static/uploads/avatar/{}.{}".format(fileName, file.filename.rsplit('.',1)[1])
        src_path = "/static/uploads/avatar/{}.{}".format(fileName, file.filename.rsplit('.',1)[1])
        file.save(os.getcwd()+file_path)
        return json.dumps({"code": 0, "msg": "", "data": {"src": src_path}})
    else:
        return json.dumps({"code": 1, "msg": "未登陆！"})