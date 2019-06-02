# -*- coding:utf-8 -*-
import os, configparser
from flask import request, render_template, json
from app import MysqlDB
from .. import admin
from ..menu import models as menuModels
from ..plugin import logic
from ..plugin import models
from app import common


@admin.route('/plugin/list', methods=['GET'])
@admin.route('/plugin/list/')
@common.login_require
def plugin_list():
    if request.method == 'GET':
        model_list = logic.get_plugin_list()
        for item in model_list:
            res = models.plugin.find_by_name(item['name'])
            if res:
                item['status'] = 1
            else:
                item['status'] = 0
        return render_template('admin/plugin/list.html', top_nav='plugin', activity_nav='plugin_list', data=model_list)


@admin.route('/plugin/install', methods=['GET', 'POST'])
@common.login_require
def plugin_install():
    title = request.form['title']
    name = request.form['name']
    config_info = logic.get_plugin_info(name)
    if config_info["code"] == 0:
        res = logic.install_plugin(name)
        if res:
            # 初始化role 并插入数据库
            role = models.plugin(title=title, name=name, status=1)
            MysqlDB.session.add(role)
            MysqlDB.session.flush()
            MysqlDB.session.commit()

            path = "{}/app/plugin/{}/config.ini".format(os.getcwd(), name)
            conf = configparser.ConfigParser()
            conf.read(path, encoding="utf-8")
            if conf.has_option("config", "config_table"):
                models.plugin.update_by_name({"name":name, "config":conf.get("config", "config_table")})

            return json.dumps({"code": 0, "msg": "完成！"})
        else:
            return json.dumps({"code": 1, "msg": res["msg"]})
    else:
        return json.dumps({"code": 1, "msg": config_info["msg"]})


@admin.route('/plugin/update', methods=['GET', 'POST'])
@common.login_require
def plugin_update():
    name = request.form['name']
    config_info = logic.update_plugin(name)
    if config_info["code"] == 0:
        return json.dumps({"code": 0, "msg": "完成！"})
    else:
        return json.dumps({"code": 1, "msg": config_info["msg"]})


@admin.route('/plugin/uninstall', methods=['GET', 'POST'])
@common.login_require
def plugin_uninstall():
    name = request.form['name']
    models.plugin.deldata_by_name(name)
    res = logic.un_install_plugin(name)
    if res:
        menuModels.menu.deldata_by_type_name(name)
        return json.dumps({"code": 0, "msg": "完成！"})
    else:
        return json.dumps({"code": 1, "msg": "失败！"})