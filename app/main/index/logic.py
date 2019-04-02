# -*- coding:utf-8 -*-
import config, json, requests, re, time
import numpy
from flask import session
from app import MongoDB
import pymongo
from app import common
from ...admin.drive import models as driveModels
from ...admin.drive import logic as driveLogic
from ...admin.author import models as authorModels
from app.admin.system import models as systemModels


"""
    URL 权限判断
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-22
    drive_id: 驱动ID
    path: 路径
"""
def author_judge(drive_id, path=''):
    if path:
        path = path[1:]
        temp = path.split('/')
        temp_path = ""
        for item in temp:
            temp_path += "/"+item
            res = authorModels.authrule.find_by_drive_id(drive_id, temp_path)
            if res:
                if res.password != session.get('password'):
                    return res
                else:
                    return
    else:
        res = authorModels.authrule.find_by_drive_id(drive_id, path)
        return res


"""
    URL 密码查询
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-22
    drive_id: 驱动ID
    path: 路径
    password: 密码
"""
def author_password(drive_id, path='', password=''):
    if path:
        path = path[1:]
        temp = path.split('/')
        temp_path = ""
        for item in temp:
            temp_path += "/"+item
            res = authorModels.authrule.find_by_drive_id(drive_id, temp_path)
            if res:
                if res.password == password:
                    return res
    else:
        res = authorModels.authrule.find_by_drive_id(drive_id, path)
        return res


"""
    获取数据列表，从MongoDB拉取
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    disk_id: disk id
    path: 路径
    search: keywords
    sortTable: 排序字段
    sortType： 排序类型  less是ASCENDING升序，more是DESCENDING降序
"""
def get_data(disk_id, path='', search='', sortTable='lastModifiedDateTime', sortType='more', page=1):
    search_type = systemModels.config.get_config('search_type')
    drivename = "drive_" + str(disk_id)
    collection = MongoDB.db[drivename]
    data = []
    if sortType == "more":
        sortType = pymongo.DESCENDING
    else:
        sortType = pymongo.ASCENDING
    if search is not None:
        result = collection.find({"name":re.compile(search)}).sort([(sortTable, sortType)])
    else:
        result = collection.find({"path": path}).sort([(sortTable, sortType)])
    for x in result:
        if search_type == "1":
            x["lastModifiedDateTime"] = str(x["lastModifiedDateTime"])
            x["createdDateTime"] = str(x["createdDateTime"])
            x["size"] = common.size_cov(x["size"])
            if x["file"] == "folder":
                data.insert(0, x)
            else:
                x["downloadUrl"] = x["downloadUrl"]
                data.append(x)
        else:
            dirve_id = driveModels.drive_list.find_by_drive_id(disk_id)[0].id
            authorres = authorModels.authrule.find_by_drive_id_all(dirve_id)
            authorpath = []
            for i in authorres:
                authorpath.append(i.path)
            if x["path"] not in authorpath:
                x["lastModifiedDateTime"] = str(x["lastModifiedDateTime"])
                x["createdDateTime"] = str(x["createdDateTime"])
                x["size"] = common.size_cov(x["size"])
                if x["file"] == "folder":
                    data.insert(0, x)
                else:
                    x["downloadUrl"] = x["downloadUrl"]
                    data.append(x)
    data = Pagination_data(data, page)
    return data


"""
    MongoDB分页内容
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-23
    data: 数据
    page: 页码
"""
def Pagination_data(data, page):
    page = int(page)
    page_number = int(systemModels.config.get_config("page_number"))
    result = []
    count = 0
    if page == 1:
        start = 0  # 第几条开始
        for item in data:
            if count >= start:
                if count < start + page_number:
                    result.append(item)
            count += 1
    else:
        start = (page-1) * page_number - 1 # 第几条开始
        for item in data:
            if count > start:
                if count <= start + page_number:
                    result.append(item)
            count += 1
    return {"data":result, "pagination":{"count": int(len(data)/page_number)+1, "page": numpy.arange(1, int(len(data)/page_number)+2), "now_page": page}}


"""
    获取数据真实地址
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-17
    drive_id: 驱动id
    disk_id: 网盘id
    res_id: 资源id
"""
def get_downloadUrl(drive_id, disk_id, id):
    data_list = driveModels.drive_list.find_by_id(disk_id)
    token = json.loads(json.loads(data_list.token))
    BaseUrl = config.app_url + 'v1.0/me/drive/items/' + id
    headers = {'Authorization': 'Bearer {}'.format(token["access_token"])}
    try:
        get_res = requests.get(BaseUrl, headers=headers, timeout=30)
        get_res = json.loads(get_res.text)
        # print(get_res)
        if 'error' in get_res.keys():
            driveLogic.reacquireToken(disk_id)
            get_downloadUrl(drive_id, disk_id, id)
        else:
            if '@microsoft.graph.downloadUrl' in get_res.keys():
                drivename = "drive_" + str(disk_id)
                collection = MongoDB.db[drivename]
                collection.update_one({"id":get_res["id"]}, {"$set": {"downloadUrl":get_res["@microsoft.graph.downloadUrl"],"timeout":int(time.time())+300}})
                return {"name": get_res["name"], "downloadUrl": get_res["@microsoft.graph.downloadUrl"]}
            else:
                get_downloadUrl(drive_id, disk_id, id)
    except:
        get_downloadUrl(drive_id, disk_id, id)


"""
    获取文件下载地址
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-17
    drive_id: 驱动id
    disk_id: 网盘id
    res_id: 资源id
"""
def file_url(drive_id, disk_id, id):
    drivename = "drive_" + str(disk_id)
    collection = MongoDB.db[drivename]
    result = collection.find_one({"id": id})
    if result["timeout"] < int(time.time()):
        get_res = get_downloadUrl(drive_id, disk_id, id)
        return {"name": get_res["name"], "url": get_res["downloadUrl"]}
    else:
        return {"name": result["name"], "url": result["downloadUrl"]}