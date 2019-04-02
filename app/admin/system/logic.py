# -*- coding:utf-8 -*-
import os, time
import configparser



"""
    Get Themes Config List
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-02
"""
def get_themes_list():
    path = os.getcwd()+"/app/templates/themes"
    path_list = os.listdir(path)
    data_list = []
    for item in path_list:
        conf = configparser.ConfigParser()
        conf.read("{}/{}/config.ini".format(path, item), encoding="utf-8")
        options = conf.items('config')
        temp = {}
        for i in options:
            temp[i[0]] = i[1]
            temp['img'] = "/static/themes/{}/cover.png".format(options[1][1])
        data_list.append(temp)
    return data_list


"""
    Modify Themes Config
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-02
    name: Themes Name
"""
def modify_themes_config(name):
    path = os.getcwd() + "/app/templates/themes"
    path_list = os.listdir(path)
    config_path = os.getcwd()+"/config.py"
    result = ''
    with open(config_path, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            if (line.find('THEMES') == 0):
                line = 'THEMES = %s' % ('\"' + name + '\"\n')
            result += line
    with open(config_path, 'w', encoding='UTF-8') as f:
        f.writelines(result)

    for item in path_list:
        conf = configparser.ConfigParser()
        conf.read("{}/{}/config.ini".format(path, item), encoding="utf-8")
        if item == name:
            conf.set("config", "status", "1")
        else:
            conf.set("config", "status", "0")
        conf.write(open("{}/{}/config.ini".format(path, item), "w"))
