# -*- coding:utf-8 -*-
import os, configparser, json, shutil
import config
from app import common
from app import MysqlDB
from ..menu import models


"""
    Get Model Config List
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def get_model_list():
    path = os.getcwd()+"/app/model"
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
    Install Model
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def install_model(name):
    admin_themes(name, True)
    revise_blueprint('{}/app/admin'.format(os.getcwd(), name), 'movie.admin', True)
    revise_blueprint('{}/app/main'.format(os.getcwd(), name), 'movie.controller', True)
    revise_views('movie', True)
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
    UnInstall Model
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def un_install_model(name):
    admin_themes(name, False)
    revise_blueprint('{}/app/admin'.format(os.getcwd(), name), 'movie.admin', False)
    revise_blueprint('{}/app/main'.format(os.getcwd(), name), 'movie.controller', False)
    revise_views('movie', False)
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
    @Time: 2019-04-25
"""
def admin_themes(model, status=True):
    model_path = "{}/app/model/{}/themes/admin".format(os.getcwd(),model)
    folder_path = "{}/app/templates/admin/model/{}".format(os.getcwd(),model)
    try:
        if status:
            if not folder_path:
                # 如果不存在则创建目录
                os.makedirs(folder_path)
            shutil.move(model_path, folder_path+"/admin")
        else:
            shutil.move(folder_path+"/admin", model_path)
            os.rmdir(folder_path)
    except:
        return False






"""
    revise Blueprint
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def revise_blueprint(path, model, status=True):
    config_path = path + '/__init__.py'
    result = ''
    ifOn = False
    try:
        if status:
            with open(config_path, 'r', encoding='UTF-8') as f:
                for line in f.readlines():
                    if (line.find('from app.model.'+model+' import views') == 0):
                        ifOn = True
                    result += line
                if ifOn is False:
                    line = '\n' + 'from app.model.'+model+' import views'
                    result += line
        else:
            with open(config_path, 'r', encoding='UTF-8') as f:
                for line in f.readlines():
                    if (line.find('from app.model.'+model+' import views') == 0):
                        line = ''
                    result += line
        with open(config_path, 'w', encoding='UTF-8') as f:
            f.writelines(result)
        return
    except:
        return False


"""
    revise views
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-25
"""
def revise_views(model, status=True):
    config_path = '{}/app/main/indexs/views.py'.format(os.getcwd())
    result = ''
    ifOn = False
    try:
        if status:
            with open(config_path, 'r', encoding='UTF-8') as f:
                for line in f.readlines():
                    if (line.find('from app.model.'+model+'.controller import views as '+model+'Views') == 0):
                        ifOn = True
                    result += line
            if ifOn is False:
                result = ''
                with open(config_path, 'r', encoding='UTF-8') as f:
                    for line in f.readlines():
                        if (line.find("THEMES = 'themes/'+ config.THEMES +'/'") == 0):
                            line += 'from app.model.'+model+'.controller import views as '+model+'Views' + '\n'
                        result += line
        else:
            with open(config_path, 'r', encoding='UTF-8') as f:
                for line in f.readlines():
                    if (line.find('from app.model.'+model+'.controller import views as '+model+'Views') == 0):
                        line = ''
                    result += line
        with open(config_path, 'w', encoding='UTF-8') as f:
            f.writelines(result)
        return
    except:
        return False