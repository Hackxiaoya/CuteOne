# -*- coding:utf-8 -*-
import config, json, requests
from flask import session
from app import MongoDB
import pymongo
from app import common
from ...admin.drive import models
from ...admin.drive import logic
from ...admin.author import models as authorModels



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
    disk_id: 驱动ID
    path: 路径
    sortTable: 排序字段
    sortType： 排序类型  less是ASCENDING升序，more是DESCENDING降序
"""
def get_data(disk_id, path='', sortTable='lastModifiedDateTime', sortType='more'):
    drivename = "drive_" + str(disk_id)
    collection = MongoDB.db[drivename]
    data = []
    if sortType == "more":
        sortType = pymongo.DESCENDING
    else:
        sortType = pymongo.ASCENDING
    result = collection.find({"path":path}).sort([(sortTable, sortType)])
    for x in result:
        x["lastModifiedDateTime"] = str(x["lastModifiedDateTime"])
        x["createdDateTime"] = str(x["createdDateTime"])
        x["size"] = common.size_cov(x["size"])
        if x["file"] == "folder":
            data.insert(0, x)
        else:
            data.append(x)
    return data


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
    data_list = models.drive_list.find_by_id(disk_id)
    token = json.loads(json.loads(data_list.token))
    BaseUrl = config.app_url + 'v1.0/me/drive/items/' + id
    headers = {'Authorization': 'Bearer {}'.format(token["access_token"])}
    try:
        get_res = requests.get(BaseUrl, headers=headers, timeout=30)
        get_res = json.loads(get_res.text)
        # print(get_res)
        if 'error' in get_res.keys():
            logic.reacquireToken(disk_id)
            get_downloadUrl(disk_id, id)
        else:
            if '@microsoft.graph.downloadUrl' in get_res.keys():
                return {"name": get_res["name"], "url": get_res["@microsoft.graph.downloadUrl"]}
            else:
                get_downloadUrl(disk_id, id)
    except:
        get_downloadUrl(disk_id, id)


"""
    获取文件下载地址
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-17
    drive_id: 驱动id
    disk_id: 网盘id
    res_id: 资源id
"""
def down_file(drive_id, disk_id, id):
    data_list = models.drive_list.find_by_id(disk_id)
    token = json.loads(json.loads(data_list.token))
    BaseUrl = config.app_url + 'v1.0/me/drive/items/' + id
    headers = {'Authorization': 'Bearer {}'.format(token["access_token"])}
    try:
        get_res = requests.get(BaseUrl, headers=headers, timeout=30)
        get_res = json.loads(get_res.text)
        # print(get_res)
        if 'error' in get_res.keys():
            logic.reacquireToken(disk_id)
            get_downloadUrl(disk_id, id)
        else:
            if '@microsoft.graph.downloadUrl' in get_res.keys():
                return {"name": get_res["name"], "url": get_res["@microsoft.graph.downloadUrl"]}
            else:
                get_downloadUrl(disk_id, id)
    except:
        get_downloadUrl(disk_id, id)