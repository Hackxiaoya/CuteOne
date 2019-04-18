# -*- coding:utf-8 -*-
import os, json, subprocess
import traceback
import pymysql
import pymongo
from flask import render_template, request, redirect
from . import index
from app import common
root_path = os.path.abspath(os.path.join(os.getcwd()))

@index.route('/')
@index.route('/index', methods=['GET', 'POST'])
def index():
    # 判断是否安装程序，避免出现重装的BUG
    if os.path.isfile(root_path + '/.install'):
        return redirect("/")
    else:
        if request.method == 'GET':
            return render_template('installer/index.html')
        else:
            from_data = request.form.to_dict()
            admin_user = from_data["admin_user"]
            admin_psw = common.hashPwd(from_data["admin_psw"])
            create_db_res = create_db(from_data["mysql_ip"], from_data["mysql_user"], from_data["mysql_psw"], from_data["mysql_port"], from_data["mysql_name"], admin_user, admin_psw)
            create_mongo_db_res = create_mongo_db(from_data["mongo_ip"], from_data["mongo_port"])
            if create_db_res and create_mongo_db_res:
                mysql_res = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(from_data["mysql_user"],
                                                                                 from_data["mysql_psw"],
                                                                                 from_data["mysql_ip"],
                                                                                 from_data["mysql_port"],
                                                                                 from_data["mysql_name"])
                mongo_res = "mongodb://{}:{}/cache".format(from_data["mongo_ip"], from_data["mongo_port"])
                edit_config(mysql_res, mongo_res)
                subprocess.Popen("python3 {}/app/task/restart.py".format(os.getcwd()), shell=True)
                return json.dumps({"code": 0, "msg": "完成！"})
            else:
                return json.dumps({"code": 1, "msg": "Mysql数据库无法连接,或者未建立,请检查后重新安装！"})



# 创建Mysql数据库
def create_db(host, user, password, port, dbname, admin_user, admin_psw):
    try:
        db = pymysql.connect(host=host, user=user, password=password, port=int(port))
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE " + str(dbname) + " DEFAULT CHARACTER SET utf8mb4")
        cursor.execute("use " + str(dbname) + ";")
        with open(root_path + "/app/main/install/install.sql", "r+", encoding="UTF-8") as f:
            sql_list = f.read().split(";")[:-1]
            sql_list = [x.replace("\n", " ") if "\n" in x else x for x in sql_list]
        for sql_item in sql_list:
            cursor.execute(sql_item)
        cursor.execute('update cuteone_config set value = "%s" where name = "username"' % (admin_user))
        cursor.execute('update cuteone_config set value = "%s" where name = "password"' % (admin_psw))
        db.commit()
        return True
    except:
        traceback.print_exc()
        return False


# 创建mongo数据库
def create_mongo_db(host, port):
    import traceback
    try:
        clinet = pymongo.MongoClient(host=host, port=int(port)) # 连接数据库
        collist = clinet.list_databases()
        if "cache" in collist:  # 判断 cache 数据库是否存在
            print("数据库已存在！")
            return True

        db = clinet['cache']    # 创建数据库
        col = db["test"]   # 创建集合
        col.insert_one({"name": "cuteone"})    # 插入集合数据，确保数据库的创建
        return True
    except:
        traceback.print_exc()
        return False


# 修改数据库链接文件
def edit_config(mysql, mongo):
    config_path = root_path + '/config.py'
    install_path = root_path + '/.install'
    result = ''
    with open(config_path, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            if (line.find('SQLALCHEMY_DATABASE_URI') == 0):
                line = 'SQLALCHEMY_DATABASE_URI = %s' % ('\"'+mysql+'\"\n')
            if (line.find('MONGO_URI') == 0):
                line = 'MONGO_URI = %s' % ('\"'+mongo+'\"\n')
            result += line
    with open(config_path, 'w', encoding='UTF-8') as f:
        f.writelines(result)
    open(install_path, 'w+').close()
    return
