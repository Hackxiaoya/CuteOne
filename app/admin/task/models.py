# -*- coding:utf-8 -*-
import time
from app import MysqlDB
from sqlalchemy import and_,or_

class task(MysqlDB.Model):
    __tablename__ = 'cuteone_task'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    description = MysqlDB.Column(MysqlDB.String(255), unique=False)
    command = MysqlDB.Column(MysqlDB.String(255), unique=False)
    stime = MysqlDB.Column(MysqlDB.String(255), unique=False)
    type = MysqlDB.Column(MysqlDB.String(255), unique=False)
    source = MysqlDB.Column(MysqlDB.String(255), unique=False)
    status = MysqlDB.Column(MysqlDB.String(255), unique=False, default=1)
    last_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
    create_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'))

    @classmethod
    def all(cls):
        data = cls.query.all()
        MysqlDB.session.close()
        return data

    # 根据ID查询出结果
    @classmethod
    def find_by_id(cls, id):
        data = cls.query.filter(cls.id == id).first()
        MysqlDB.session.close()
        return data

    @classmethod
    def find_status(cls, status):
        data = cls.query.filter(cls.status == status).all()
        MysqlDB.session.close()
        return data


    @classmethod
    def deldata(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.delete(data)
        MysqlDB.session.commit()
        MysqlDB.session.flush()
        MysqlDB.session.close()
        return


    @classmethod
    def update(cls, data):
        MysqlDB.session.query(cls).filter(cls.id == data['id']).update(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        return


class uploads_list(MysqlDB.Model):
    __tablename__ = 'cuteone_uploads_list'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    drive_id = MysqlDB.Column(MysqlDB.String(255), unique=False)
    file_name = MysqlDB.Column(MysqlDB.String(255), unique=False)
    type = MysqlDB.Column(MysqlDB.String(255), unique=False)
    path = MysqlDB.Column(MysqlDB.String(255), unique=False)
    status = MysqlDB.Column(MysqlDB.String(255), unique=False, default=1)
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
    create_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'))

    @classmethod
    def all(cls):
        data = cls.query.all()
        MysqlDB.session.close()
        return data

    # 根据ID查询出结果
    @classmethod
    def find_by_id(cls, id):
        data = cls.query.filter(cls.id == id).first()
        MysqlDB.session.close()
        return data


    @classmethod
    def deldata(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.delete(data)
        MysqlDB.session.commit()
        MysqlDB.session.flush()
        MysqlDB.session.close()
        return


    # 根据驱动ID获取规则列表
    @classmethod
    def find_by_drive_id(cls, drive_id, path):
        data = MysqlDB.session.query(cls).filter(and_(cls.drive_id == drive_id, or_(cls.path == '', cls.path == path))).first()
        MysqlDB.session.close()
        return data


    @classmethod
    def update(cls, data):
        MysqlDB.session.query(cls).filter(cls.id == data['id']).update(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        return