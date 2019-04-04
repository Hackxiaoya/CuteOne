# -*- coding:utf-8 -*-
import os, sys, json, threading, requests, time
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
from app import MongoDB
from app.admin.drive import logic
from app.admin.drive import models as driveModels
from app.admin.task import models as taskModels
import config
from app.task.syn import down, uploads
from app import common

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
    contrast_dif(drive_id)  # 差异对比
    collection = MongoDB.db[drivename]
    time.sleep(3)
    driveData = getMongoDB(drivename)
    for item in driveData:
        if item["syn_disk"]:
            common.send_socket(drive_id, "{} | 拉取 {} 的下载地址".format(time.strftime('%Y-%m-%d %H:%M:%S'), item["name"]))
            # 拉取下载地址
            down_info = pull_dirve_file(chief_id, item["id"])
            if down_info is None:   # 报错二次拉取
                down_info = pull_dirve_file(chief_id, item["id"])
            common.send_socket(drive_id, "{} | 拉取 {} 的下载地址完成".format(time.strftime('%Y-%m-%d %H:%M:%S'), item["name"]))
            # 下载文件
            down_result = down.down_file(down_info["url"], down_info["name"], drive_id)
            # 下载文件完成
            if down_result:
                # print("Start Syn File: " + item["name"])
                common.send_socket(drive_id, "{} | 开始同步 {}".format(time.strftime('%Y-%m-%d %H:%M:%S'), item["name"]))
                # 同步到各个盘
                uploads.upProcess(drive_id, down_info["name"], item["path"])
                common.send_socket(drive_id, "{} | 同步 {} 完成，删除同步缓存数据ID".format(time.strftime('%Y-%m-%d %H:%M:%S'), item["name"]))
                # 删除缓存数据库数据
                collection.delete_one({"id": item["id"]})

    MongoDB.db[drivename].remove()  # 移除集合所有数据
    MongoDB.db[drivename].drop()  # 删除集合
    common.send_socket(drive_id, "{} | 同步完成！".format(time.strftime('%Y-%m-%d %H:%M:%S')))
    # print("完成下载")


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
    thread_list = []  # 线程存放列表
    try:
        # 创建集合 - 不添加一条数据，集合是不会创建的，因为MongoDB是惰性数据库
        drivename = "syn_drive_" + str(drive_id)
        collection = MongoDB.db[drivename]
        for i in res["data"]["value"]:
            if "folder" in i.keys():
                common.send_socket(drive_id, "{} | 拉取 {} 缓存数据".format(time.strftime('%Y-%m-%d %H:%M:%S'), i["name"]))
                dic = {
                    "id": i["id"],
                    "parentReference": i["parentReference"]["id"],
                    "name": i["name"],
                    "file": "folder",
                    "path": i["parentReference"]["path"].replace("/drive/root:", "")
                }
                collection.insert_one(dic)
                t = threading.Thread(target=task_getlist, args=(disk_id, "/" + path + "/" + i["name"], drive_id,))
                thread_list.append(t)
            else:
                t = threading.Thread(target=task_write, args=(drive_id, i,))
                thread_list.append(t)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
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
    common.send_socket(drive_id, "{} | 入库 {}".format(time.strftime('%Y-%m-%d %H:%M:%S'), data["name"]))
    # 创建集合 - 不添加一条数据，集合是不会创建的，因为MongoDB是惰性数据库
    drivename = "syn_drive_" + str(drive_id)
    collection = MongoDB.db[drivename]
    dic = {
        "id": data["id"],
        "parentReference": data["parentReference"]["id"],
        "name": data["name"],
        "file": data["file"]["mimeType"],
        "path": data["parentReference"]["path"].replace("/drive/root:", ""),
        "syn_disk": []
    }
    collection.insert_one(dic)


"""
    获取文件下载地址
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
    except Exception as e:
        pass
        # print(e)
        # pull_dirve_file(chief_id, file_id)


"""
    读取MongoDB SYN数据
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-03-23
    dbName: 集和名称
"""
def getMongoDB(dbName):
    collection = MongoDB.db[dbName]
    result = collection.find()
    data = []
    for x in result:
        if x["file"] != "folder":
            data.append(x)
    return data


"""
    对比差异
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-04
    drive_id: 驱动id
"""
def contrast_dif(drive_id):
    common.send_socket(drive_id, "{} | 开始对比差异".format(time.strftime('%Y-%m-%d %H:%M:%S')))
    disk_list = driveModels.drive_list.find_by_drive_id(drive_id)
    disk_list_res = []
    # 列出缓存集
    for item in disk_list:
        if item.chief != "1":
            disk_list_res.append("drive_"+str(item.id))
    # 缓存集差异对比
    for dbname in disk_list_res:
        collectionList = MongoDB.db.list_collection_names()
        if dbname in collectionList:  # 如果存在集合，就进行差异对比
            contrast_dif_one_disk(dbname, drive_id)
        else:
            disk_id = dbname.replace("drive_", "")
            common.send_socket(drive_id, "{} | 发现差异，Disk_id: {}".format(time.strftime('%Y-%m-%d %H:%M:%S'), disk_id))
            synDb = MongoDB.db["syn_drive_" + str(drive_id)]
            synDb_data = synDb.find()
            for item in synDb_data:
                if item["file"] != "folder":
                    syn_disk = item["syn_disk"]
                    if disk_id not in syn_disk:
                        syn_disk.append(disk_id)
                        synDb.update_one({"name": item["name"], "path": item["path"]}, {"$set": {"syn_disk": syn_disk}})
    common.send_socket(drive_id, "{} | 对比差异完成".format(time.strftime('%Y-%m-%d %H:%M:%S')))


"""
    单库对比差异
    @Author: yyyvy <76836785@qq.com>
    @Description:
    @Time: 2019-04-04
    dbname: 缓存网盘集和名称
    drive_id: 驱动ID
"""
def contrast_dif_one_disk(dbname, drive_id):
    synDb = getMongoDB("syn_drive_" + str(drive_id))
    disk_id = dbname.replace("drive_", "")
    for item in synDb:
        thread_dif_one(item["name"], item["path"], drive_id, disk_id)


def thread_dif_one(name, path, drive_id, disk_id):
    collection = MongoDB.db["drive_" + str(disk_id)]
    res = collection.find_one({"name": name, "path": path})
    if res is None:
        synDb = MongoDB.db["syn_drive_" + str(drive_id)]
        common.send_socket(drive_id, "{} | 发现差异，Disk_id: {}".format(time.strftime('%Y-%m-%d %H:%M:%S'), disk_id))
        synDb_get_one = synDb.find_one({"name": name, "path": path})
        syn_disk = synDb_get_one["syn_disk"]
        if disk_id not in syn_disk:
            syn_disk.append(disk_id)
            synDb.update_one({"name": name, "path": path}, {"$set": {"syn_disk": syn_disk}})


if __name__ =='__main__':
    drive_id = sys.argv[1]  # 驱动ID
    pull_chief_dirve_info(drive_id)

    # while True:
    #     print("1")
    #     time.sleep(5)