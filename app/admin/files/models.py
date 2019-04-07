# -*- coding:utf-8 -*-
import time
from app import MysqlDB
from sqlalchemy import and_,or_

class files(MysqlDB.Model):
    __tablename__ = 'cuteone_files'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    uid = MysqlDB.Column(MysqlDB.String(255), unique=False)
    disk_id = MysqlDB.Column(MysqlDB.String(255), unique=False)
    type = MysqlDB.Column(MysqlDB.String(255), unique=False)
    name = MysqlDB.Column(MysqlDB.String(255), unique=False)
    file = MysqlDB.Column(MysqlDB.String(255), unique=False)
    size = MysqlDB.Column(MysqlDB.String(255), unique=False)
    files_id = MysqlDB.Column(MysqlDB.String(255), unique=False)
    status = MysqlDB.Column(MysqlDB.String(255), unique=False)
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


    # 分页
    @classmethod
    def get_pages(cls, uid, page_index, page_size):
        page_index = int(page_index)
        page_size = int(page_size)
        data = []
        result_folder = MysqlDB.session.query(cls).filter(cls.uid == uid, cls.file == 'folder').order_by(cls.update_time.asc()).all()
        result = MysqlDB.session.query(cls).filter(cls.uid == uid, cls.file != 'folder').order_by(cls.update_time.asc()).limit(page_size).offset((page_index - 1) * page_size).all()
        for item in result_folder:
            json_data = {
                "id": item.id,
                "uid": item.uid,
                "disk_id": item.disk_id,
                "type": item.type,
                "name": item.name,
                "size": item.size,
                "file": item.file,
                "files_id": item.files_id,
                "status": item.status,
                "update_time": item.update_time
            }
            data.append(json_data)
        for item in result:
            json_data = {
                "id": item.id,
                "uid": item.uid,
                "disk_id": item.disk_id,
                "type": item.type,
                "name": item.name,
                "size": item.size,
                "file": item.file,
                "files_id": item.files_id,
                "status": "可用" if item.status else "不可用",
                "update_time": item.update_time
            }
            data.append(json_data)
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


class filesDisk(MysqlDB.Model):
    __tablename__ = 'cuteone_files_disk'
    id = MysqlDB.Column(MysqlDB.INT, primary_key=True)
    title = MysqlDB.Column(MysqlDB.String(255), unique=False)
    description = MysqlDB.Column(MysqlDB.String(255), unique=False)
    client_id = MysqlDB.Column(MysqlDB.String(255), unique=False)
    client_secret = MysqlDB.Column(MysqlDB.String(255), unique=False)
    token = MysqlDB.Column(MysqlDB.String(255), unique=False)
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


    @classmethod
    def update(cls, data):
        MysqlDB.session.query(cls).filter(cls.id == data['id']).update(data)
        MysqlDB.session.flush()
        MysqlDB.session.commit()
        return