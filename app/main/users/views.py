# -*- coding:utf-8 -*-
import time, json, random
from flask import render_template, request, redirect, url_for
import app
from flask_login import login_user, logout_user
from app.admin.users import models as usersModels
from app.admin.author import models as authorModels
from app import MysqlDB
from ..users import users
from app import common
import config
THEMES = 'themes/'+ config.THEMES +'/'




@users.route('/login', methods=['GET', 'POST'])  # Login
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
            model.group = authorModels.authGroup.find_by_id(res["msg"].group).title
            login_user(model)
            return json.dumps({"code": 0, "msg": "登陆成功！"})
        else:
            return json.dumps({"code": 1, "msg": res["msg"]})


@users.route('/register', methods=['GET', 'POST'])  # Register
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
            group = 1,
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



@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index._index'))
