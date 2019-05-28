# -*- coding:utf-8 -*-
import os, configparser, json, shutil
from app import common
from app import MysqlDB
from ..menu import models
from ..model import models as modelsModels
from ..plugin import models as pluginModels
from ..hooks import models as hooksModels


"""
    Get Model Config List
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def get_model_list():
    path = os.getcwd()+"/app/model"
    path_list = os.listdir(path)
    for p in path_list:
        if os.path.isdir(os.getcwd()+"/app/model/"+p) is False:
            path_list.remove(p)
    data_list = []
    for item in path_list:
        conf = configparser.ConfigParser()
        conf.read("{}/{}/config.ini".format(path, item), encoding="utf-8")
        options = conf.items('config')
        temp = {}
        for i in options:
            temp[i[0]] = i[1]
        data_list.append(temp)
    return data_list


"""
    Get Model Config Info
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def get_model_info(name):
    path = "{}/app/model/{}/config.ini".format(os.getcwd(), name)
    conf = configparser.ConfigParser()
    conf.read(path, encoding="utf-8")
    system_version = conf.get('config', 'system_version')
    system_version = system_version.split(" ")
    systemInfo = common.SystemInfo["versions"]
    current_version = int(systemInfo.replace(".", ""))
    new_version = int(system_version[1].replace(".", ""))
    if system_version[0] == ">=":
        if current_version < new_version and current_version != new_version:
            return {"code":1, "msg":"系统版本要大于等于 "+system_version[1]}
    elif system_version[0] == "<=":
        if current_version > new_version and current_version != new_version:
            return {"code":1, "msg":"系统版本要小于等于 "+system_version[1]}
    elif system_version[0] == "=":
        if current_version[1] != new_version:
            return {"code":1, "msg":"系统版本要等于 "+system_version[1]}
    if conf.has_option("config", "depend_model"):
        depend_model = eval(conf.get('config', 'depend_model'))
        for m in depend_model:
            m_find_res = modelsModels.model.find_by_name(m)
            if m_find_res is None:
                return {"code":1, "msg":"请先安装 " + m + "模块！" }
    if conf.has_option("config", "depend_plugin"):
        depend_plugin = eval(conf.get('config', 'depend_plugin'))
        for p in depend_plugin:
            p_find_res = pluginModels.plugin.find_by_name(p)
            if p_find_res is None:
                return {"code": 1, "msg": "请先安装 " + p + "插件！"}
    return {"code": 0, "msg": ""}





"""
    Install Model
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def install_model(name):
    admin_themes(name, True)
    hook(name, True)
    model_path = '{}/app/model/{}/install/'.format(os.getcwd(), name)
    if os.path.isfile(model_path+"install.sql"):
        try:
            cursor = MysqlDB
            with open(model_path+"install.sql", "r+", encoding="UTF-8") as f:
                sql_list = f.read().split(";")[:-1]
                sql_list = [x.replace("\n", " ") if "\n" in x else x for x in sql_list]
            for sql_item in sql_list:
                cursor.session.execute(sql_item)
            cursor.session.commit()
        except Exception as e:
            return False

    if os.path.isfile(model_path + "menu.json"):
        with open(model_path + "menu.json", "r", encoding="UTF-8") as menu_file:
            res = menu_file.read().replace("\n", "")
        menu_data = json.loads(res)
        for i in menu_data:
            if i == "in_menu":
                postion = 0
            else:
                postion = 1
            for v in menu_data[i]:
                if "icon" in v.keys():
                    icon = v["icon"]
                else:
                    icon = "fa fa-cube"
                role = models.menu(title=v["title"], postion=postion, url=v["url"], icon=icon, top_nav=v["top_nav"], activity_nav=v["activity_nav"], type=2, type_name=name, activate=0, sort=0, status=1)
                MysqlDB.session.add(role)
                MysqlDB.session.flush()
                pid = role.id
                MysqlDB.session.commit()
                if len(v["children"]) > 0:
                    for x in v["children"]:
                        if "icon" in x.keys():
                            icon = str(v["icon"])
                        else:
                            icon = ""
                        two_role = models.menu(title=x["title"], pid=pid, postion=postion, icon=icon, top_nav=x["top_nav"], activity_nav=x["activity_nav"], url=x["url"], type=2, type_name=name, activate=0, sort=0, status=1)
                        MysqlDB.session.add(two_role)
                        MysqlDB.session.flush()
                        MysqlDB.session.commit()
    return True


"""
    UnInstall Model
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def un_install_model(name):
    admin_themes(name, False)
    hook(name, False)
    model_path = '{}/app/model/{}/install/'.format(os.getcwd(), name)
    if os.path.isfile(model_path+"uninstall.sql"):
        try:
            cursor = MysqlDB
            with open(model_path+"uninstall.sql", "r+", encoding="UTF-8") as f:
                sql_list = f.read().split(";")[:-1]
                sql_list = [x.replace("\n", " ") if "\n" in x else x for x in sql_list]
            for sql_item in sql_list:
                cursor.session.execute(sql_item)
            cursor.session.commit()
        except Exception as e:
            return False
    models.menu.deldata_by_type_name(name)
    return True


"""
    Admin Themes
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-05-25
"""
def admin_themes(name, status=True):
    model_themes = "{}/app/model/{}/themes".format(os.getcwd(), name)
    model_templates = "{}/app/templates/model/{}".format(os.getcwd(), name)
    model_static = "{}/app/model/{}/static".format(os.getcwd(), name)
    static_path = "{}/app/static/model/{}".format(os.getcwd(), name)
    try:
        if status:
            if os.path.isdir(model_themes):
                if os.path.isdir(model_templates) is False:
                    # 如果不存在则创建目录
                    os.makedirs(model_templates)
                if os.path.isdir(model_themes + "/admin"):
                    shutil.move(model_themes + "/admin", model_templates + "/admin")
                if os.path.isdir(model_themes + "/front"):
                    shutil.move(model_themes + "/front", model_templates + "/front")
            if os.path.isdir(model_static):
                shutil.move(model_static, static_path)

        else:
            if os.path.isdir(model_templates + "/admin"):
                shutil.move(model_templates + "/admin", model_themes + "/admin")
            if os.path.isdir(model_templates + "/front"):
                shutil.move(model_templates + "/front", model_themes + "/front")
            if os.path.isdir(static_path):
                shutil.move(static_path, model_static)
    except:
        return False


"""
    Hooks
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-29
"""
def hook(name, status=True):
    plugin_path = '{}/app/model/{}/hook.json'.format(os.getcwd(), name)
    if status:
        if os.path.isfile(plugin_path):
            with open(plugin_path, "r", encoding="UTF-8") as menu_file:
                res = menu_file.read().replace("\n", "")
                res = res.replace(" ", "")
            menu_data = json.loads(res)
            for i in menu_data["list"]:
                role = hooksModels.hooks(title=i["title"], description=i["description"], source=name, type=1, method=i["method"], status=1)
                MysqlDB.session.add(role)
                MysqlDB.session.flush()
                MysqlDB.session.commit()
    else:
        hooksModels.hooks.deldata_by_source(name, 1)
    return True