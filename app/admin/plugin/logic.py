# -*- coding:utf-8 -*-
import os, configparser, json, shutil, requests, zipfile
from app import common
from app import MysqlDB
from ..menu import models
from ..model import models as modelsModels
from ..plugin import models as pluginModels
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
    for p in path_list:
        if os.path.isdir(os.getcwd()+"/app/plugin/"+p) is False:
            path_list.remove(p)
    data_list = []
    for item in path_list:
        conf = configparser.ConfigParser()
        conf.read("{}/{}/config.ini".format(path, item), encoding="utf-8")
        options = conf.items('config')
        temp = {}
        for i in options:
            temp[i[0]] = i[1]
        cloud_update = detect_update(temp["name"], temp["version"])
        temp["cloud_update"] = cloud_update
        data_list.append(temp)
    return data_list


"""
    Detect cloud update status
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-6-1
    name: name
    version: version
"""
def detect_update(name, version):
    try:
        server_url = common.SystemInfo["server"] + "cuteone/expand/get_expand"
        data = {
            'name': name,
            'types': 2
        }
        get_res = requests.post(server_url, data=data)
        get_res = json.loads(get_res.text)
        if get_res["code"] == 4:
            return 4
        if get_res["code"] == 0:
            for i in get_res["data"]["version"]:
                if i["version"] > version:
                    return 1    # 云端有新版
            return 2    # 云端无新版
        else:
            return 0    # 云端无此扩展
    except Exception as e:
        return 3


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
    current_version = int(systemInfo.replace(".", ""))
    new_version = int(system_version[1].replace(".", ""))
    if system_version[0] == ">=":
        if current_version < new_version and current_version != new_version:
            return {"code":1, "msg":"系统版本要大于等于 "+system_version[1]}
    elif system_version[0] == "<=":
        if current_version > new_version and current_version != new_version:
            return {"code": 1, "msg": "系统版本要小于等于 " + system_version[1]}
    elif system_version[0] == "=":
        if current_version[1] != new_version:
            return {"code": 1, "msg": "系统版本要等于 " + system_version[1]}
    if conf.has_option("config", "depend_model"):
        depend_model = eval(conf.get('config', 'depend_model'))
        for m in depend_model:
            m_find_res = modelsModels.model.find_by_name(m)
            if m_find_res is None:
                return {"code": 1, "msg": "请先安装 " + m + "模块！"}
    if conf.has_option("config", "depend_plugin"):
        depend_plugin = eval(conf.get('config', 'depend_plugin'))
        for p in depend_plugin:
            p_find_res = pluginModels.plugin.find_by_name(p)
            if p_find_res is None:
                return {"code": 1, "msg": "请先安装 " + p + "插件！"}
    return {"code": 0, "msg": ""}


"""
    Install Plugin
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def install_plugin(name):
    try:
        server_url = common.SystemInfo["server"] + "cuteone/expand/get_expand"
        get_res = requests.post(server_url, data={'name': name, 'types': 2})
        get_res = json.loads(get_res.text)
        if get_res["code"] == 4:
            return {"code": 1, "msg": "error"}
    except:
            return {"code": 1, "msg": "云端请求错误"}
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
            return {"code": 1, "msg": e}

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
                            icon = x["icon"]
                        else:
                            icon = ""
                        two_role = models.menu(title=x["title"], pid=pid, postion=postion, icon=icon, top_nav=x["top_nav"], activity_nav=x["activity_nav"], url=x["url"], type=2, type_name=name, activate=0, sort=0, status=1)
                        MysqlDB.session.add(two_role)
                        MysqlDB.session.flush()
                        MysqlDB.session.commit()
    return {"code": 0, "msg": "成功"}


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
    update Plugin
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def update_plugin(name):
    try:
        server_url = common.SystemInfo["server"] + "cuteone/expand/get_expand"
        get_res = requests.post(server_url, data={'name': name, 'types': 2})
        get_res = json.loads(get_res.text)
        if get_res["code"] == 4:
            return {"code": 1, "msg": "error"}
    except:
        return {"code": 1, "msg": "云端请求错误"}
    path = "{}/app/plugin/{}/config.ini".format(os.getcwd(), name)
    conf = configparser.ConfigParser()
    conf.read(path, encoding="utf-8")
    version = conf.get('config', 'version')
    admin_themes(name, False)   # 移回释放文件
    # 备份旧版
    try:
        backup_path = "{}/app/backup_path/plugin/{}/{}".format(os.getcwd(), name, version)
        plugin_path = "{}/app/plugin/{}".format(os.getcwd(), name)
        if os.path.isdir(backup_path) is False:
            # 如果不存在则创建目录
            os.makedirs(backup_path)
        shutil.move(plugin_path, backup_path)
    except:
        return {"code": 1, "msg": "备份文件出错，应该是权限不足"}
    # 拉取新版
    for n in get_res["data"]:
        if n["version"] > version:
            down_res = requests.get(n["file"])
            update_file = "{}/app/plugin/{}.zip".format(os.getcwd(), name)
            with open(update_file, "wb") as f:
                f.write(down_res.content)
            f = zipfile.ZipFile(update_file, 'r')
            for file in f.namelist():
                f.extract(file, "{}/app/plugin".format(os.getcwd()))
            admin_themes(name, True)    # 从新释放
    return {"code": 0, "msg": "成功"}


"""
    Admin Themes
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-05-25
"""
def admin_themes(name, status=True):
    model_path = "{}/app/plugin/{}/themes".format(os.getcwd(), name)
    folder_path = "{}/app/templates/plugin/{}".format(os.getcwd(), name)
    plugin_static = "{}/app/model/{}/static".format(os.getcwd(), name)
    static_path = "{}/app/static/plugin/{}".format(os.getcwd(), name)
    try:
        if status:
            if os.path.isdir(model_path):
                if os.path.isdir(folder_path) is False:
                    # 如果不存在则创建目录
                    os.makedirs(folder_path)
                if os.path.isdir(model_path + "/admin"):
                    shutil.move(model_path + "/admin", folder_path + "/admin")
                if os.path.isdir(model_path + "/front"):
                    shutil.move(model_path + "/front", folder_path + "/front")
            if os.path.isdir(plugin_static):
                shutil.move(plugin_static, static_path)
        else:
            if os.path.isdir(folder_path + "/admin"):
                shutil.move(folder_path + "/admin", model_path + "/admin")
            if os.path.isdir(folder_path + "/front"):
                shutil.move(folder_path + "/front", model_path + "/front")
            if os.path.isdir(static_path):
                shutil.move(static_path, plugin_static)
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