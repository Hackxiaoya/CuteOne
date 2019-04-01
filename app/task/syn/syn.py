# -*- coding:utf-8 -*-
import os, sys, json, threading, requests, time
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
from app import MongoDB
from app.admin.drive import logic
from app.admin.drive import models as driveModels
from app.admin.task import models as taskModels
import config
from app.task.syn import down, uploads

"""
    主从同步
"""


"""
    拉取主盘数据
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-23
    drive_id: 驱动id
"""
def pull_chief_dirve_info(drive_id):
    drivename = "syn_drive_" + str(drive_id)
    collectionList = MongoDB.db.list_collection_names()
    chief_id = driveModels.drive_list.find_by_chief(drive_id).id    # 查询主盘
    if drivename not in collectionList: # 如果不存在集合，就进行主盘信息拉取
        task_getlist(chief_id, '', drive_id)
    collection = MongoDB.db[drivename]
    time.sleep(3)
    dirveData = getMongoDB(drive_id)
    for item in dirveData:
        # 拉取下载地址
        down_info = pull_dirve_file(chief_id, item["id"])
        print("Start Down File: " + item["name"])
        # 下载文件
        down_result = down.down_file(down_info["url"], down_info["name"], drive_id)
        # 下载文件完成
        if down_result:
            print("Start Syn File: " + item["name"])
            # 同步到各个盘
            uploads.upProcess(drive_id, down_info["name"], item["path"])
            # 删除缓存数据库数据
            collection.delete_one({"id": item["id"]})

    MongoDB.db[drivename].remove()  # 移除集合所有数据
    MongoDB.db[drivename].drop()  # 删除集合
    print("完成下载")


"""
    获取文件列表
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-24
    disk_id: 网盘ID
    path: 路径
"""
def task_getlist(disk_id, path, drive_id):
    if path:
        path = path
    else:
        path = ''
    res = logic.get_one_file_list(disk_id, path)
    try:
        # 创建集合 - 不添加一条数据，集合是不会创建的，因为MongoDB是惰性数据库
        drivename = "syn_drive_" + str(drive_id)
        collection = MongoDB.db[drivename]
        for i in res["data"]["value"]:
            if "folder" in i.keys():
                dic = {
                    "id": i["id"],
                    "parentReference": i["parentReference"]["id"],
                    "name": i["name"],
                    "file": "folder",
                    "path": i["parentReference"]["path"].replace("/drive/root:", "")
                }
                collection.insert_one(dic)
                t = threading.Thread(target=task_getlist, args=(disk_id, "/" + path + "/" + i["name"], drive_id,))
                t.start()
            else:
                t = threading.Thread(target=task_write, args=(drive_id, i,))
                t.start()
    except:
        task_getlist(disk_id, path, drive_id)


"""
    添加syn主盘数据到MongoDB
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-24
    disk_id: 驱动ID
    data: 数据
"""
def task_write(disk_id, data):
    # 创建集合 - 不添加一条数据，集合是不会创建的，因为MongoDB是惰性数据库
    drivename = "syn_drive_" + str(disk_id)
    collection = MongoDB.db[drivename]
    dic = {
        "id": data["id"],
        "parentReference": data["parentReference"]["id"],
        "name": data["name"],
        "file": data["file"]["mimeType"],
        "path": data["parentReference"]["path"].replace("/drive/root:", "")
    }
    collection.insert_one(dic)


"""
    获取文件下载地址， 顺带下载
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-23
    chief_id: 主盘id
    file_id: 文件id
"""
def pull_dirve_file(chief_id, file_id):
    data_list = driveModels.drive_list.find_by_id(chief_id)
    token = json.loads(json.loads(data_list.token))
    BaseUrl = config.app_url + 'v1.0/me/drive/items/' + file_id
    headers = {'Authorization': 'Bearer {}'.format(token["access_token"])}
    try:
        get_res = requests.get(BaseUrl, headers=headers, timeout=30)
        get_res = json.loads(get_res.text)
        if 'error' in get_res.keys():
            logic.reacquireToken(chief_id)
            pull_dirve_file(chief_id, file_id)
        else:
            if '@microsoft.graph.downloadUrl' in get_res.keys():
                return {"name": get_res["name"], "url": get_res["@microsoft.graph.downloadUrl"]}
            else:
                pull_dirve_file(chief_id, file_id)
    except:
        pull_dirve_file(chief_id, file_id)


"""
    读取MongoDB主盘数据
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-23
    disk_id: 驱动id
"""
def getMongoDB(disk_id):
    drivename = "syn_drive_" + str(disk_id)
    collection = MongoDB.db[drivename]
    result = collection.find()
    data = []
    for x in result:
        if x["file"] != "folder":
            data.append(x)
    return data


if __name__ =='__main__':
    drive_id = sys.argv[1]  # 驱动ID
    pull_chief_dirve_info(drive_id)
    # while True:
    #     print("1")
    #     time.sleep(5)