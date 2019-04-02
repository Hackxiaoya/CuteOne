# -*- coding:utf-8 -*-
import os, sys, json, threading, time
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
from app import MongoDB
from app.admin.drive import logic
from app.admin.drive import models
from app import common

"""
    后台任务
"""

"""
    获取文件列表
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    id: 网盘ID
    path: 路径
    type: 类型
"""
def task_getlist(id, path, type):
    if path:
        path = path
    else:
        path = ''
    res = logic.get_one_file_list(id, path)
    try:
        # 创建集合 - 不添加一条数据，集合是不会创建的，因为MongoDB是惰性数据库
        drivename = "drive_" + str(id)
        collection = MongoDB.db[drivename]
        for i in res["data"]["value"]:
            if type == "all":
                if "folder" in i.keys():
                    dic = {
                        "id": i["id"],
                        "parentReference": i["parentReference"]["id"],
                        "name": i["name"],
                        "file": "folder",
                        "path": i["parentReference"]["path"].replace("/drive/root:", ""),
                        "size": i["size"],
                        "createdDateTime": common.utc_to_local(i["fileSystemInfo"]["createdDateTime"]),
                        "lastModifiedDateTime": common.utc_to_local(i["fileSystemInfo"]["lastModifiedDateTime"])
                    }
                    collection.insert_one(dic)
                    t = threading.Thread(target=task_getlist, args=(id, "/" + path + "/" + i["name"], type,))
                    t.start()
                else:
                    t = threading.Thread(target=task_write, args=(id, i, type,))
                    t.start()
            else:
                if "folder" in i.keys():
                    if collection.find_one({"id": i["id"]}):
                        t = threading.Thread(target=task_getlist, args=(id, "/" + path + "/" + i["name"], type,))
                        t.start()
                    else:
                        dic = {
                            "id": i["id"],
                            "parentReference": i["parentReference"]["id"],
                            "name": i["name"],
                            "file": "folder",
                            "path": i["parentReference"]["path"].replace("/drive/root:", ""),
                            "size": i["size"],
                            "createdDateTime": common.utc_to_local(i["fileSystemInfo"]["createdDateTime"]),
                            "lastModifiedDateTime": common.utc_to_local(i["fileSystemInfo"]["lastModifiedDateTime"])
                        }
                        collection.insert_one(dic)
                        t = threading.Thread(target=task_getlist, args=(id, "/" + path + "/" + i["name"], type,))
                        t.start()
                else:
                    t = threading.Thread(target=task_write, args=(id, i, type,))
                    t.start()
    except:
        task_getlist(id, path, type)


"""
    添加缓存数据到MongoDB
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-16
    types: 类型
"""
def task_write(id, data, type):
    # 创建集合 - 不添加一条数据，集合是不会创建的，因为MongoDB是惰性数据库
    drivename = "drive_" + str(id)
    collection = MongoDB.db[drivename]
    if type == "all":
        dic = {
            "id": data["id"],
            "parentReference": data["parentReference"]["id"],
            "name": data["name"],
            "file": data["file"]["mimeType"],
            "path": data["parentReference"]["path"].replace("/drive/root:", ""),
            "size": data["size"],
            "createdDateTime": common.utc_to_local(data["fileSystemInfo"]["createdDateTime"]),
            "lastModifiedDateTime": common.utc_to_local(data["fileSystemInfo"]["lastModifiedDateTime"]),
            "downloadUrl": data["@microsoft.graph.downloadUrl"],
            "timeout": int(time.time()) + 300
        }
        collection.insert_one(dic)
    else:
        if collection.find_one({"id": data["id"]}) is None:
            dic = {
                "id": data["id"],
                "parentReference": data["parentReference"]["id"],
                "name": data["name"],
                "file": data["file"]["mimeType"],
                "path": data["parentReference"]["path"].replace("/drive/root:", ""),
                "size": data["size"],
                "createdDateTime": common.utc_to_local(data["fileSystemInfo"]["createdDateTime"]),
                "lastModifiedDateTime": common.utc_to_local(data["fileSystemInfo"]["lastModifiedDateTime"]),
                "downloadUrl": data["@microsoft.graph.downloadUrl"],
                "timeout": int(time.time()) + 300
            }
            collection.insert_one(dic)
        else:
            collection.update_one({"id": data["id"]}, {
                "$set": {"downloadUrl": data["@microsoft.graph.downloadUrl"], "timeout": int(time.time()) + 300}})


if __name__ =='__main__':
    id = sys.argv[1]  # 驱动ID
    type = sys.argv[2]  # 更新类型，all全部，dif差异
    if type == "all":   # 如果是更新全部
        drivename = "drive_" + str(id)
        MongoDB.db[drivename].remove() # 移除集合所有数据
        MongoDB.db[drivename].drop()   # 删除集合
    task_getlist(id, '', type)