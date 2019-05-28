# -*- coding:utf-8 -*-
import os, pymysql, sys
import app
root_path = os.path.abspath(os.path.join(os.getcwd()))




# 创建Mysql数据库
def create_db(host, user, password, port, dbname):
    try:
        db = pymysql.connect(host=host, user=user, password=password, port=int(port))
        cursor = db.cursor()
        # cursor.execute("CREATE DATABASE " + str(dbname) + " DEFAULT CHARACTER SET utf8")
        cursor.execute("use " + str(dbname) + ";")
        with open(root_path + "/app/main/install/install.sql", "r+", encoding="UTF-8") as f:
            sql_list = f.read().split(";")[:-1]
            sql_list = [x.replace("\n", " ") if "\n" in x else x for x in sql_list]
        for sql_item in sql_list:
            cursor.execute(sql_item)
        # cursor.execute('update cuteone_config set value = "%s" where name = "username"' % (admin_user))
        # cursor.execute('update cuteone_config set value = "%s" where name = "password"' % (admin_psw))
        # db.commit()
        return True
    except Exception as e:
        return False


# 修改数据库链接文件
def edit_config(mysql, mongo):
    config_path = root_path + '/config.py'
    install_path = root_path + '/.install'
    result = ''
    with open(config_path, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            if (line.find('SQLALCHEMY_DATABASE_URI') == 0):
                line = 'SQLALCHEMY_DATABASE_URI = %s' % ('\"' + mysql + '\"\n')
            if (line.find('MONGO_URI') == 0):
                line = 'MONGO_URI = %s' % ('\"' + mongo + '\"')
            result += line
    with open(config_path, 'w', encoding='UTF-8') as f:
        f.writelines(result)
    open(install_path, 'w+').close()
    return



if __name__ == '__main__':
    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    port = sys.argv[4]
    dbname = sys.argv[5]
    create_db(host, user, password, port, dbname)
    mysql_res = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(user,password,host,port,dbname)
    mongo_res = "mongodb://{}:{}/cache".format("127.0.0.1", "27017")
    edit_config(mysql_res, mongo_res)