# -*- coding:utf-8 -*-
import os, configparser, json, shutil
import config
from app import common
from app import MysqlDB
from ..menu import models
from ..hooks import models as hooksModels


"""
    Get Plugin Config List
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def get_plugin_list():
    path = os.getcwd()+"/app/plugin"
    path_list = os.listdir(path)
    path_list.remove("README.md")
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
    Get Plugin Config Info
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def get_plugin_info(name):
    path = "{}/app/plugin/{}/config.ini".format(os.getcwd(), name)
    conf = configparser.ConfigParser()
    conf.read(path, encoding="utf-8")
    system_version = conf.get('config', 'system_version')
    system_version = system_version.split(" ")
    systemInfo = common.SystemInfo["versions"]
    if system_version[0] == ">=":
        if systemInfo >= system_version[1]:
            return True
        else:
            return False
    elif system_version[0] == "<=":
        if systemInfo <= system_version[1]:
            return True
        else:
            return False
    elif system_version[0] == "=":
        if system_version[1] == systemInfo:
            return True
        else:
            return False


"""
    Install Plugin
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def install_plugin(name):
    admin_themes(name, True)
    hook(name, True)
    model_path = '{}/app/plugin/{}/install/'.format(os.getcwd(), name)
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
            res = res.replace(" ", "")
        menu_data = json.loads(res)
        for i in menu_data:
            if i == "in_menu":
                postion = 0
            else:
                postion = 1
            for v in menu_data[i]:
                role = models.menu(title=v["title"], postion=postion, url=v["url"], top_nav=v["top_nav"], activity_nav=v["activity_nav"], type=2, type_name=name, activate=0, sort=0, status=1)
                MysqlDB.session.add(role)
                MysqlDB.session.flush()
                pid = role.id
                MysqlDB.session.commit()
                if len(v["children"]) > 0:
                    for x in v["children"]:
                        two_role = models.menu(title=x["title"], pid=pid, postion=postion, top_nav=x["top_nav"], activity_nav=x["activity_nav"], url=x["url"], type=2, type_name=name, activate=0, sort=0, status=1)
                        MysqlDB.session.add(two_role)
                        MysqlDB.session.flush()
                        MysqlDB.session.commit()
    return True


"""
    UnInstall Plugin
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def un_install_plugin(name):
    admin_themes(name, False)
    hook(name, False)
    model_path = '{}/app/plugin/{}/install/'.format(os.getcwd(), name)
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
    @Time: 2019-04-25
"""
def admin_themes(name, status=True):
    model_path = "{}/app/plugin/{}/themes/admin".format(os.getcwd(), name)
    folder_path = "{}/app/templates/admin/plugin/{}".format(os.getcwd(), name)
    try:
        if status:
            if os.path.isdir(model_path):
                if os.path.isdir(folder_path) is False:
                    # 如果不存在则创建目录
                    os.makedirs(folder_path)
                shutil.move(model_path, folder_path+"/admin")
        else:
            shutil.move(folder_path+"/admin", model_path)
            os.rmdir(folder_path)
    except:
        return False


"""
    Hooks
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-29
"""
def hook(name, status=True):
    plugin_path = '{}/app/plugin/{}/hook.json'.format(os.getcwd(), name)
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