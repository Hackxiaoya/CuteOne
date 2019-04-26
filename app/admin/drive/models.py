# -*- coding:utf-8 -*-
import time, json
from app import MysqlDB
from app import MongoDB
from sqlalchemy import and_,or_



class drive(MysqlDB.Model):
    __tablename__ = 'cuteone_drive'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    description = MysqlDB.Column(MysqlDB.String(255), unique=False)
    update_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'), onupdate=time.strftime('%Y-%m-%d %H:%M:%S'))
    create_time = MysqlDB.Column(MysqlDB.DateTime(255), default=time.strftime('%Y-%m-%d %H:%M:%S'))

    """
        all
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


    # 获取设定主页的驱动
    @classmethod
    def find_activate(cls):
        data = MysqlDB.session.query(cls).filter(cls.activate == "1").first()
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
        data = MysqlDB.session.query(cls).filter(cls.drive_id == drive_id).order_by(cls.create_time.desc()).all()
        MysqlDB.session.close()
        return data

    # 根据ID查询出结果
    @classmethod
    def find_by_id(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        MysqlDB.session.close()
        return data


    # 根据drive_id查询列表
    @classmethod
    def find_by_drive_id(cls, drive_id):
        data =  MysqlDB.session.query(cls).filter(cls.drive_id == drive_id).all()
        MysqlDB.session.close()
        return data

    # 根据drive_id查询主盘
    @classmethod
    def find_by_chief(cls, drive_id):
        data = MysqlDB.session.query(cls).filter(and_(cls.drive_id == drive_id, cls.chief == 1)).first()
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
    def deldata_by_id(cls, id):
        data = MysqlDB.session.query(cls).filter(cls.id == id).first()
        mongodb_del_drive(data.id)
        MysqlDB.session.delete(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        MysqlDB.session.close()
        return


    @classmethod
    def deldata_by_drive_id(cls, drive_id):
        data = MysqlDB.session.query(cls).filter(cls.drive_id == drive_id).all()
        for item in data:
            mongodb_del_drive(item.id)
            MysqlDB.session.delete(item)
            MysqlDB.session.flush()
            MysqlDB.session.commit()
        MysqlDB.session.close()
        return



# 删除MongoDB的表
def mongodb_del_drive(id):
    drivename = "drive_" + str(id)
    MongoDB.db[drivename].remove()  # 移除集合所有数据
    MongoDB.db[drivename].drop()  # 删除集合
    return

# 查询MongoDB的指定缓存表数据总数
def mongodb_count(id):
    drivename = "drive_" + str(id)
    return MongoDB.db[drivename].count()  # 查询总数

# 查询MongoDB的指定网盘指定路径ID
def mongodb_find_parent_id(id, path):
    collection = "drive_" + str(id)
    res = json.dumps(collection.find({"path": path}))
    return res["id"]