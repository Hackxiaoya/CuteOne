# -*- coding:utf-8 -*-
from flask import render_template, session, request, json, redirect
from app.admin import admin
from app import common
from ..system import models
from app import decorators


@admin.route('/index/login', methods=['GET', 'POST'])  # 登录页
def login():
    if request.method == 'GET':
        return render_template('admin/index/login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        password = common.hashPwd(password)
        res = models.config.checkpassword(username, password)
        if res["code"]:
            session['is_login'] = True
            session['username'] = username
            return json.dumps({"code": 0, "msg": "登录成功，正在跳转..."})
        else:
            return json.dumps({"code": 1, "msg": res["msg"]})


@admin.route('/index/logout', methods=['GET'])  # 注销登录
def logout():
    session.pop('is_login')
    return redirect("admin/index/login")



@admin.route('/')  # 后台首页
@admin.route('/index')  # 后台首页
@decorators.login_require
def _index():
    return render_template('admin/index/index.html', activity_nav='index', data='')

