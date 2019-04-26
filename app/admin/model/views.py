# -*- coding:utf-8 -*-
from flask import request, render_template, json
from app import MysqlDB
from .. import admin
from ..menu import models as menuModels
from ..model import logic
from ..model import models
from app import decorators



@admin.route('/model/list', methods=['GET'])
@admin.route('/model/list/')
@decorators.login_require
def model_list():
    if request.method == 'GET':
        model_list = logic.get_model_list()
        for item in model_list:
            res = models.model.find_by_name(item['name'])
            if res:
                item['status'] = 1
            else:
                item['status'] = 0
        return render_template('admin/model/list.html', top_nav='model', activity_nav='model_list', data=model_list)


@admin.route('/model/install', methods=['GET', 'POST'])
@decorators.login_require
def model_install():
    title = request.form['title']
    name = request.form['name']
    config_info = logic.get_model_info(name)
    if config_info:
        res = logic.install_model(name)
        if res:
            # 初始化role 并插入数据库
            role = models.model(title=title, name=name, status=1)
            MysqlDB.session.add(role)
            MysqlDB.session.flush()
            MysqlDB.session.commit()
            return json.dumps({"code": 0, "msg": "完成！"})
        else:
            return json.dumps({"code": 1, "msg": "失败！"})
    else:
        return json.dumps({"code": 1, "msg": "系统版本太低！"})


@admin.route('/model/uninstall', methods=['GET', 'POST'])
@decorators.login_require
def model_uninstall():
    name = request.form['name']
    models.model.deldata_by_name(name)
    res = logic.un_install_model(name)
    if res:
        menuModels.menu.deldata_by_type_name(name)
        return json.dumps({"code": 0, "msg": "完成！"})
    else:
        return json.dumps({"code": 1, "msg": "失败！"})