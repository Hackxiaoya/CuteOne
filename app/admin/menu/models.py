# -*- coding:utf-8 -*-
import time
from app import MysqlDB
from sqlalchemy import and_,or_

class menu(MysqlDB.Model):
    __tablename__ = 'cuteone_menu'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    pid = MysqlDB.Column(MysqlDB.String(255), unique=False)
    postion = MysqlDB.Column(MysqlDB.String(255), unique=False)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    url = MysqlDB.Column(MysqlDB.String(255), unique=False)
    icon = MysqlDB.Column(MysqlDB.String(255), unique=False)
    top_nav = MysqlDB.Column(MysqlDB.String(255), unique=False)
    activity_nav = MysqlDB.Column(MysqlDB.String(255), unique=False)
    type = MysqlDB.Column(MysqlDB.String(255), unique=False, default=0)
    type_name = MysqlDB.Column(MysqlDB.String(255), unique=False)
    activate = MysqlDB.Column(MysqlDB.String(255), unique=False)
    sort = MysqlDB.Column(MysqlDB.String(255), unique=False)
    status = MysqlDB.Column(MysqlDB.String(255), unique=False)
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
    create_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'))


    """
        postion: postion
        sort: 1是降序，2是升序
        status: 
    """
    @classmethod
    def all(cls, postion=0, sort=1, status=1):
        if sort == 1:
            order_by = menu.sort.desc()
        else:
            order_by = menu.sort.asc()
        if status == 0:
            status = cls.status == 0
        elif status == 1:
            status = cls.status == 1
        else:
            status = or_(cls.status == 0, cls.status == 1)
        data = MysqlDB.session.query(cls).filter(and_(cls.postion==postion, status)).order_by(order_by).all()
        MysqlDB.session.close()
        return data

    # 根据ID查询出结果
    @classmethod
    def find_by_id(cls, id):
        data = cls.query.filter(cls.id == id).first()
        MysqlDB.session.close()
        return data


    @classmethod
    def find_by_index(cls):
        data = cls.query.filter(cls.activate == 1).first()
        MysqlDB.session.close()
        return data


    @classmethod
    def deldata_by_title_type(cls, title, type):
        data = MysqlDB.session.query(cls).filter(and_(cls.title == title, cls.type == type)).first()
        MysqlDB.session.delete(data)
        MysqlDB.session.commit()
        MysqlDB.session.flush()
        MysqlDB.session.close()
        return


    @classmethod
    def deldata_by_type_name(cls, type_name):
        MysqlDB.session.query(cls).filter(cls.type_name == type_name).delete()
        MysqlDB.session.commit()
        MysqlDB.session.flush()
        MysqlDB.session.close()
        return


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
