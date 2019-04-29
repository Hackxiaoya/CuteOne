# -*- coding:utf-8 -*-
import time
from app import MysqlDB
from sqlalchemy import and_,or_

class model(MysqlDB.Model):
    __tablename__ = 'cuteone_model'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    name = MysqlDB.Column(MysqlDB.String(255), unique=False)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    config = MysqlDB.Column(MysqlDB.String(255), unique=False)
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
    def find_by_name(cls, name):
        data = MysqlDB.session.query(cls).filter(cls.name == name).first()
        MysqlDB.session.close()
        return data


    @classmethod
    def update_by_name(cls, data):
        MysqlDB.session.query(cls).filter(cls.name == data['name']).update(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        return


    @classmethod
    def deldata(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.delete(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        MysqlDB.session.close()
        return


    @classmethod
    def deldata_by_name(cls, name):
        data = MysqlDB.session.query(cls).filter(cls.name == name).first()
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