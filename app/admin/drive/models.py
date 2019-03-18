# -*- coding:utf-8 -*-
import time
from app import MysqlDB
from sqlalchemy import and_,or_



class drive(MysqlDB.Model):
    __tablename__ = 'cuteone_drive'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    activate = MysqlDB.Column(MysqlDB.String(255), unique=False)
    sort = MysqlDB.Column(MysqlDB.String(255), unique=False)
    description = MysqlDB.Column(MysqlDB.String(255), unique=False)
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
    create_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'))

    """
        table: sort 要么留空
        sort: 1是降序，2是升序
    """
    @classmethod
    def all(cls, table="", sort=""):
        if table == "sort":
            if sort == 1:
                order_by = drive.sort.desc()
            else:
                order_by = drive.sort.asc()
        else:
            order_by = drive.create_time.desc()
        data = drive.query.order_by(order_by).all()
        MysqlDB.session.close()
        return data


    # 根据ID查询出结果
    @classmethod
    def find_by_id(cls, id):
        data =  drive.query.filter(drive.id == id).first()
        MysqlDB.session.close()
        return data


    # 获取设定主页的驱动
    @classmethod
    def find_activate(cls):
        data = drive.query.filter(drive.activate == "1").first()
        MysqlDB.session.close()
        return data


    @classmethod
    def update(cls, data):
        drive.query.filter(drive.id == data['id']).update(data)
        MysqlDB.session.commit()
        return


class drive_list(MysqlDB.Model):
    __tablename__ = 'cuteone_drive_list'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    drive_id = MysqlDB.Column(MysqlDB.String(255), unique=False)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    client_id = MysqlDB.Column(MysqlDB.String(255), unique=False)
    client_secret = MysqlDB.Column(MysqlDB.String(255), unique=False)
    token = MysqlDB.Column(MysqlDB.String(255), unique=False)
    chief = MysqlDB.Column(MysqlDB.String(255), unique=False)
    status = MysqlDB.Column(MysqlDB.String(255), unique=False)
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
    create_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'))

    @classmethod
    def all(cls, drive_id):
        data = drive_list.query.filter(drive_list.drive_id == drive_id).order_by(drive_list.create_time.desc()).all()
        MysqlDB.session.close()
        return data

    # 根据ID查询出结果
    @classmethod
    def find_by_id(cls, id):
        data = drive_list.query.filter(drive_list.id == id).first()
        MysqlDB.session.close()
        return data


    # 根据drive_id查询出结果
    @classmethod
    def find_by_drive_id(cls, drive_id):
        data =  drive_list.query.filter(drive_list.drive_id == drive_id).all()
        MysqlDB.session.close()
        return data


    # 根据drive_id查询主盘
    @classmethod
    def find_by_chief(cls, drive_id):
        data = drive_list.query.filter(and_(drive_list.drive_id == drive_id, drive_list.chief == 1)).first()
        MysqlDB.session.close()
        return data


    @classmethod
    def update(cls, data):
        drive_list.query.filter(drive_list.id == data['id']).update(data)
        MysqlDB.session.commit()
        return