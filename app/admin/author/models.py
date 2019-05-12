# -*- coding:utf-8 -*-
import time
from app import MysqlDB
from sqlalchemy import and_,or_

class authrule(MysqlDB.Model):
    __tablename__ = 'cuteone_auth_rule'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    drive_id = MysqlDB.Column(MysqlDB.String(255), unique=False)
    path = MysqlDB.Column(MysqlDB.String(255), unique=False)
    password = MysqlDB.Column(MysqlDB.String(255), unique=False)
    login_hide = MysqlDB.Column(MysqlDB.String(255), unique=False)
    status = MysqlDB.Column(MysqlDB.String(255), unique=False, default=1)
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
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
    def deldata(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.delete(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        MysqlDB.session.close()
        return


    # 根据驱动ID获取规则列表
    @classmethod
    def find_by_drive_id(cls, drive_id, path):
        data = MysqlDB.session.query(cls).filter(and_(cls.drive_id == drive_id, or_(cls.path == '', cls.path == path))).first()
        MysqlDB.session.close()
        return data

    # 根据ID，驱动ID,路径获取规则
    @classmethod
    def find_by_id_drive_path(cls, id, drive_id, path):
        data = MysqlDB.session.query(cls).filter(
            and_(cls.id == id, cls.drive_id == drive_id, or_(cls.path == '', cls.path == path))).first()
        MysqlDB.session.close()
        return data


    # 根据驱动ID获取规则列表
    @classmethod
    def find_by_drive_id_all(cls, drive_id):
        data = MysqlDB.session.query(cls).filter(cls.drive_id == drive_id).all()
        MysqlDB.session.close()
        return data

    @classmethod
    def update(cls, data):
        MysqlDB.session.query(cls).filter(cls.id == data['id']).update(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        return


class authGroup(MysqlDB.Model):
    __tablename__ = 'cuteone_auth_group'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    auth_group = MysqlDB.Column(MysqlDB.String(255), unique=False)
    description = MysqlDB.Column(MysqlDB.String(255), unique=False)
    price = MysqlDB.Column(MysqlDB.String(255), unique=False)
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
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
    def deldata(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.delete(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        MysqlDB.session.close()
        return


    @classmethod
    def update(cls, data):
        MysqlDB.session.query(cls).filter(cls.id == data['id']).update(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        return