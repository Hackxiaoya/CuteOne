# -*- coding:utf-8 -*-
import config, json, requests, re, time
import math
import numpy
from flask import session
from app import MongoDB
import pymongo
from app import common
from flask_login import current_user
from ...admin.drive import models as driveModels
from ...admin.drive import logic as driveLogic
from ...admin.author import models as authorModels
from ...admin.system import models as systemModels
from ...admin.users import models as usersModels


"""
    URL 权限判断
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-22
    drive_id: 驱动ID
    users_id: 会员ID
    path: 路径
"""
def author_judge(drive_id, users_id='', path=''):
    if path:
        path = path[1:]
        temp = path.split('/')
        temp_path = ""
        for item in temp:
            temp_path += "/" + item

        if users_id:    # 如果是会员
            group_id = usersModels.users.find_by_id(users_id).group
            if group_id == 0:
                res = authorModels.authrule.find_by_drive_id(drive_id, temp_path)
                if res:
                    if res.password != session.get(temp_path):
                        return True
                    else:
                        return False
            else:
                res = authorModels.authrule.find_by_drive_id(drive_id, temp_path)
                if res:
                    group_data = authorModels.authGroup.find_by_id(group_id).auth_group
                    group_data = group_data.split(",")
                    for item in group_data:
                        res = authorModels.authrule.find_by_id_drive_path(item, drive_id, temp_path)
                        if res is not None:
                            return False
                    return True
                else:
                    return False
        else:
            res = authorModels.authrule.find_by_drive_id(drive_id, temp_path)
            if res:
                if res.password != session.get(temp_path):
                    return True
                else:
                    return False
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
    drive_id = driveModels.drive_list.find_by_id(disk_id).id
    authorres = authorModels.authrule.find_by_drive_id_all(drive_id)
    authorpath = [] # 权限路径信息数组
    for i in authorres:
        authorpath.append({"path":i.path, "login_hide":i.login_hide})
    search_type = systemModels.config.get_config('search_type')
    drivename = "drive_" + str(disk_id)
    collection = MongoDB.db[drivename]
    data = []
    if sortType == "more":
        sortType = pymongo.DESCENDING
    else:
        sortType = pymongo.ASCENDING
    if search is None:
        result = collection.find({"path": path}).sort([(sortTable, sortType)])
        for x in result:
            x["lastModifiedDateTime"] = str(x["lastModifiedDateTime"])
            x["createdDateTime"] = str(x["createdDateTime"])
            x["size"] = common.size_cov(x["size"])
            if x["file"] == "folder":
                author_if_res = True
                if current_user.get_id() is not None:
                    for a in authorpath:
                        if x["path"]=="" and x["name"] == a["path"].strip("/") and a["login_hide"] == 1 and a["login_hide"] == 2:
                            author_if_res = False
                            exit()
                        elif x["path"] == a["path"] and a["login_hide"] == 1 and a["login_hide"] == 2:
                            author_if_res = False
                else:
                    for a in authorpath:
                        if x["path"]=="" and x["name"] == a["path"].strip("/") and a["login_hide"] == 2:
                            author_if_res = False
                        elif x["path"] == a["path"] and a["login_hide"] == 1:
                            author_if_res = False
                if author_if_res:
                    data.insert(0, x)
            else:
                x["downloadUrl"] = x["downloadUrl"]
                data.append(x)
    else:
        result = collection.find({"name":re.compile(search)}).sort([(sortTable, sortType)])
        for x in result:
            if search_type == "1":
                x["lastModifiedDateTime"] = str(x["lastModifiedDateTime"])
                x["createdDateTime"] = str(x["createdDateTime"])
                x["size"] = common.size_cov(x["size"])
                if x["file"] == "folder":
                    author_if_res = True
                    if current_user.get_id() is not None:
                        for a in authorpath:
                            if x["name"] == a["path"].strip("/") and a["login_hide"] == 1 and a["login_hide"] == 2:
                                author_if_res = False
                    else:
                        for a in authorpath:
                            if x["name"] == a["path"].strip("/") and a["login_hide"] == 2:
                                author_if_res = False
                    if author_if_res:
                        data.insert(0, x)
                else:
                    x["downloadUrl"] = x["downloadUrl"]
                    data.append(x)
            else:
                x["lastModifiedDateTime"] = str(x["lastModifiedDateTime"])
                x["createdDateTime"] = str(x["createdDateTime"])
                x["size"] = common.size_cov(x["size"])
                if x["file"] == "folder":
                    author_if_res = True
                    if current_user.get_id() is not None:
                        for a in authorpath:
                            if x["path"] == "" and x["name"] == a["path"].strip("/") and a["login_hide"] == 1 and a[
                                "login_hide"] == 2:
                                author_if_res = False
                                exit()
                            elif x["path"] == a["path"] and a["login_hide"] == 1 and a["login_hide"] == 2:
                                author_if_res = False
                    else:
                        for a in authorpath:
                            if x["path"] == "" and x["name"] == a["path"].strip("/") and a["login_hide"] == 2:
                                author_if_res = False
                            elif x["path"] == a["path"] and a["login_hide"] == 1:
                                author_if_res = False
                    if author_if_res:
                        data.insert(0, x)
                else:
                    x["downloadUrl"] = x["downloadUrl"]
                    data.append(x)
    data = Pagination_data(data, page)
    return data


"""
    内容隐藏
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-05
    data: 内容
"""
def hidedata(data):
    if int(len(data)/2) > 12:
        return data.replace(data[5:16], '****')
    if int(len(data)/2) > 9:
        return data.replace(data[5:16], '****')
    if int(len(data)/2) > 7:
        return data.replace(data[5:14], '****')
    elif int(len(data)/2) > 5:
        return data.replace(data[3:7], '****')
    elif int(len(data)/2) > 2:
        return data.replace(data[2:4], '****')



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
    if len(list(range(1, math.ceil(len(data) / page_number) + 2))) > 10:
        if int(page) > 2:
            if int(page) < math.ceil(len(data) / page_number) + 1:
                if int(page) < math.ceil(len(data) / page_number) -2:
                    all_page = [1, int(page)-1, page , int(page)+1, int(len(data) / page_number) + 1]
                else:
                    all_page = [1, int(page) - 1, page, int(page) + 1]
            else:
                all_page = [1, int(page) - 2, int(page) - 1, int(len(data) / page_number) + 1]
            print(all_page)
        else:
            all_page = [1, 2, 3, 4, math.ceil(len(data) / page_number) + 1]
    else:
        all_page = list(range(1, math.ceil(len(data) / page_number) + 1))
    return {"data": result, "pagination": {"count": math.ceil(len(data) / page_number), "page": all_page, "now_page": page}}


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
    get_res = requests.get(BaseUrl, headers=headers, timeout=30)
    get_res = json.loads(get_res.text)
    if 'error' in get_res.keys():
        driveLogic.reacquireToken(disk_id)
        return get_downloadUrl(drive_id, disk_id, id)
    else:
        if '@microsoft.graph.downloadUrl' in get_res.keys():
            drivename = "drive_" + str(disk_id)
            collection = MongoDB.db[drivename]
            collection.update_one({"id":get_res["id"]}, {"$set": {"downloadUrl":get_res["@microsoft.graph.downloadUrl"],"timeout":int(time.time())+300}})
            return {"name": get_res["name"], "downloadUrl": get_res["@microsoft.graph.downloadUrl"]}
        else:
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
    if int(result["timeout"]) <= int(time.time()):
        get_res = get_downloadUrl(drive_id, disk_id, id)
        return {"name": get_res["name"], "url": get_res["downloadUrl"]}
    else:
        return {"name": result["name"], "url": result["downloadUrl"]}

"""
    获取文件负载下载地址
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-17
    drive_id: 驱动id
    disk_id: 网盘id
    source_disk_id: 来源网盘id
    source_id: 来源资源id
"""
def get_load(drive_id, disk_id, source_disk_id, source_id):
    source_collection = MongoDB.db["drive_" + str(source_disk_id)]
    source_result = source_collection.find_one({"id": source_id})
    drivename = "drive_" + str(disk_id)
    collection = MongoDB.db[drivename]
    result = collection.find_one({"name": source_result["name"], "path": source_result["path"]})
    return result["id"]