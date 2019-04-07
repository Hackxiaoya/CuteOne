# -*- coding:utf-8 -*-
import time
from app import MysqlDB, login_manager
from app.admin.author import models as authorModels
from sqlalchemy import and_,or_

class users(MysqlDB.Model):
    __tablename__ = 'cuteone_users'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    username = MysqlDB.Column(MysqlDB.String(255), unique=False)
    password = MysqlDB.Column(MysqlDB.String(255), unique=False)
    nickname = MysqlDB.Column(MysqlDB.String(255), unique=False)
    email = MysqlDB.Column(MysqlDB.String(255), unique=False)
    mobile = MysqlDB.Column(MysqlDB.String(255), unique=False)
    avatar = MysqlDB.Column(MysqlDB.String(255), unique=False)
    sex = MysqlDB.Column(MysqlDB.String(255), unique=False)
    birthday = MysqlDB.Column(MysqlDB.String(255), unique=False)
    description = MysqlDB.Column(MysqlDB.String(255), unique=False)
    register_ip = MysqlDB.Column(MysqlDB.String(255), unique=False)
    login_num = MysqlDB.Column(MysqlDB.String(255), unique=False)
    last_login_ip = MysqlDB.Column(MysqlDB.String(255), unique=False)
    last_login_time = MysqlDB.Column(MysqlDB.String(255), unique=False)
    score = MysqlDB.Column(MysqlDB.String(255), unique=False)
    group = MysqlDB.Column(MysqlDB.String(255), unique=False)
    files_disk_id = MysqlDB.Column(MysqlDB.String(255), unique=False)
    status = MysqlDB.Column(MysqlDB.String(255), unique=False)
    reg_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'))
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))


    """
        
    """
    @classmethod
    def all(cls):
        data = MysqlDB.session.query(cls).all()
        MysqlDB.session.close()
        return data


    # 根据ID查询出结果
    @classmethod
    def find_by_id(cls, id):
        data =  MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.close()
        return data

    @classmethod
    def check_username(cls, name):
        data =  MysqlDB.session.query(cls).filter(cls.username == name).first()
        MysqlDB.session.close()
        return data

    @classmethod
    def update(cls, data):
        MysqlDB.session.query(cls).filter(cls.id == data['id']).update(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        MysqlDB.session.close()
        return

    @classmethod
    def deldata(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.delete(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        MysqlDB.session.close()
        return

    # 校正账号密码是否正确
    @classmethod
    def checkpassword(cls, username, password, ip):
        result = MysqlDB.session.query(cls).filter(cls.username == username).first()
        MysqlDB.session.close()
        if result:
            if result.password == password:
                if result.status == 0:
                    return {"code": False, "msg": "帐号被禁止"}
                else:
                    cls.update({
                        "id": result.id,
                        "login_num": int(result.login_num)+1,
                        "last_login_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "last_login_ip": ip
                    })
                    return {"code": True, "msg": result}
            else:
                return {"code": False, "msg": "密码错误"}
        else:
            return {"code": False, "msg": "账号错误"}


    # 分页
    @classmethod
    def get_pages(cls, page_index, page_size):
        page_index = int(page_index)
        page_size = int(page_size)
        data = MysqlDB.session.query(cls).limit(page_size).offset((page_index - 1) * page_size).all()
        MysqlDB.session.close()
        return data


    # 下面这4个方法是flask_login需要的4个验证方式
    def is_authenticated(cls):
        return True

    def is_active(cls):
        return True

    def is_anonymous(cls):
        return False

    def get_id(cls):
        return cls.id


class funds(MysqlDB.Model):
    __tablename__ = 'cuteone_funds'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    uid = MysqlDB.Column(MysqlDB.String(255), unique=False)
    content = MysqlDB.Column(MysqlDB.String(255), unique=False)
    status = MysqlDB.Column(MysqlDB.String(255), unique=False)
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'),
                                 onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
    create_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'))

    @classmethod
    def all(cls):
        data = MysqlDB.session.query(cls).all()
        MysqlDB.session.close()
        return data

    # 根据ID查询出结果
    @classmethod
    def find_by_id(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.close()
        return data

    @classmethod
    def update(cls, data):
        MysqlDB.session.query(cls).filter(cls.id == data['id']).update(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        MysqlDB.session.close()
        return

    @classmethod
    def deldata(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.delete(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        MysqlDB.session.close()
        return


@login_manager.user_loader
def load_user(user_id):
    res = users.find_by_id(user_id)
    model = users()  # 实例化一个对象，将查询结果逐一添加给对象的属性
    model.id = res.id
    model.username = res.username
    model.avatar = res.avatar
    model.nickname = res.nickname
    model.score = res.score
    if res.group:
        model.group = authorModels.authGroup.find_by_id(res.group).title
    else:
        model.group = "普通会员"
    return model

