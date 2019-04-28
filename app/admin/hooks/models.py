# -*- coding:utf-8 -*-
import time
from app import MysqlDB
from sqlalchemy import and_,or_

class hooks(MysqlDB.Model):
    __tablename__ = 'cuteone_hooks'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    description = MysqlDB.Column(MysqlDB.String(255), unique=False)
    source = MysqlDB.Column(MysqlDB.String(255), unique=False)
    type = MysqlDB.Column(MysqlDB.String(255), unique=False)
    method = MysqlDB.Column(MysqlDB.String(255), unique=False)
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
    def find_by_title(cls, title):
        data = MysqlDB.session.query(cls).filter(cls.title == title).first()
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
    def deldata_by_source(cls, name, type):
        MysqlDB.session.query(cls).filter(cls.source == name, cls.type == type).delete()
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