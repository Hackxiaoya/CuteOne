# -*- coding:utf-8 -*-
import config, json, requests
from app import MongoDB
from app import common
from ...admin.drive import models
from ...admin.drive import logic
"""
    前台MongoDB数据
"""



"""
    获取数据列表，从MongoDB拉取
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    disk_id: 驱动ID
    path: 路径
"""
def get_disk(disk_id, path=''):
    drivename = "drive_" + str(disk_id)
    collection = MongoDB.db[drivename]
    data = []
    for x in collection.find({"path":path}):
        x["lastModifiedDateTime"] = str(x["lastModifiedDateTime"])
        x["createdDateTime"] = str(x["createdDateTime"])
        x["size"] = common.size_cov(x["size"])
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
